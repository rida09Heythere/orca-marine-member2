from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None


def build_fallback_answer(prompt: str, tool_result: dict) -> str:
    """
    Generate a safe fallback response when the LLM API is unavailable.
    """

    unavailable = tool_result.get(
        "unavailable_results",
        []
    )

    errors = tool_result.get(
        "errors",
        []
    )

    fishing = tool_result.get(
        "fishing_analysis"
    )

    weather = tool_result.get(
        "weather_analysis"
    )

    # Combined fishing + weather response
    if fishing and weather:

        suitability = fishing.get(
            "suitability",
            "UNKNOWN"
        )

        score = fishing.get(
            "score",
            0
        )

        max_score = fishing.get(
            "max_score",
            3
        )

        factors = fishing.get(
            "factors",
            {}
        )

        assessment = weather.get(
            "assessment",
            "UNKNOWN"
        )

        weather_factors = weather.get(
            "factors",
            {}
        )

        return (
            f"Fishing suitability for the requested "
            f"location is {suitability}. "

            f"The prototype analysis scored "
            f"{score}/{max_score} based on "

            f"mock sea surface temperature "
            f"({factors.get('sst_c')} °C), "

            f"chlorophyll-a concentration "
            f"({factors.get('chlorophyll_mg_m3')} mg/m³), "

            f"and PFZ confidence "
            f"({factors.get('pfz_confidence')}). "

            f"Weather conditions are classified as "
            f"{assessment} by the prototype weather "
            f"assessment, based on wind speed of "
            f"{weather_factors.get('wind_speed_kmh')} km/h "
            f"and wave height of "
            f"{weather_factors.get('wave_height_m')} m. "

            f"These results use ORCA mock data and "
            f"must not be treated as real-world "
            f"fishing or marine safety advice."
        )

    # Fishing analysis only
    if fishing:

        suitability = fishing.get(
            "suitability",
            "UNKNOWN"
        )

        score = fishing.get(
            "score",
            0
        )

        max_score = fishing.get(
            "max_score",
            3
        )

        factors = fishing.get(
            "factors",
            {}
        )

        return (
            f"Fishing suitability for the requested "
            f"location is {suitability}. "

            f"The prototype analysis scored "
            f"{score}/{max_score} based on "

            f"mock sea surface temperature "
            f"({factors.get('sst_c')} °C), "

            f"chlorophyll-a concentration "
            f"({factors.get('chlorophyll_mg_m3')} mg/m³), "

            f"and PFZ confidence "
            f"({factors.get('pfz_confidence')}). "

            f"This result uses ORCA mock data and "
            f"should not be treated as a real-world "
            f"fishing recommendation."
        )

    # Weather analysis only
    if weather:

        assessment = weather.get(
            "assessment",
            "UNKNOWN"
        )

        weather_factors = weather.get(
            "factors",
            {}
        )

        return (
            f"The prototype weather assessment "
            f"classifies the marine conditions as "
            f"{assessment}. "

            f"Wind speed is "
            f"{weather_factors.get('wind_speed_kmh')} km/h "
            f"and wave height is "
            f"{weather_factors.get('wave_height_m')} m. "

            f"This assessment uses ORCA mock data and "
            f"must not be treated as real-world "
            f"marine safety advice."
        )

    # Check restricted zones
    restricted = [
        result
        for result in tool_result.get(
            "available_results",
            []
        )
        if result.get("status") == "RESTRICTED"
    ]

    if restricted:
        return (
            "CRITICAL SAFETY ALERT: The vessel is "
            "inside a restricted marine zone. "
            "The vessel should not continue operating "
            "within this restricted area."
        )

    # Check approaching zones
    approaching = [
        result
        for result in tool_result.get(
            "available_results",
            []
        )
        if result.get("status") == "APPROACHING"
    ]

    if approaching:
        return (
            "WARNING: The vessel is approaching a "
            "restricted marine zone. Exercise caution "
            "and maintain a safe distance from the "
            "boundary."
        )

    # Handle errors
    if errors:
        return (
            "I could not process the marine query "
            "completely because the provided location "
            "or tool request contains an error."
        )

    # Handle unavailable data
    if unavailable:

        tool_names = [
            result.get(
                "tool",
                "unknown"
            )
            for result in unavailable
        ]

        tools_text = ", ".join(
            tool_names
        )

        return (
            f"Marine data for {tools_text} is "
            "currently unavailable for the "
            "requested location. Therefore, "
            "I cannot reliably determine "
            "fishing suitability or marine "
            "safety conditions from these "
            "data sources yet."
        )

    return (
        "The marine tools returned results, "
        "but no LLM-generated interpretation "
        "is currently available."
    )


def ask_llm(
    prompt: str,
    tool_result: dict | None = None
) -> str:

    if tool_result:

        prompt = f"""
User question:
{prompt}

Deterministic marine tool results:
{tool_result}

Explain ALL relevant tool results clearly
to the user.

Do not invent coordinates, distances,
boundaries, weather conditions, fish abundance,
or other facts that are not present in the
tool results.

If a tool reports DATA_UNAVAILABLE,
explicitly state that the data cannot
currently be used.

If fishing analysis is provided, explain
the fishing factors.

If weather analysis is provided, explain
the weather assessment and its factors.

If the data is mock/prototype data, clearly
state that it is not real-world marine advice.

The deterministic tool results must be
treated as authoritative.
"""

    if client is None:

        if tool_result:
            return build_fallback_answer(
                prompt,
                tool_result
            )

        return (
            "The language model is currently "
            "unavailable. Please try again later."
        )

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception:

        if tool_result:
            return build_fallback_answer(
                prompt,
                tool_result
            )

        return (
            "The language model is currently "
            "unavailable. Please try again later."
        )