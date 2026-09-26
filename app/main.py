from fastapi import FastAPI

from app.models.query import UserQuery
from app.models.response import ORCAResponse
from app.services.llm import ask_llm

from app.agents.safety_agent import safety_agent
from app.agents.result_summarizer import summarize_results
from app.agents.fishing_agent import fishing_agent
from app.agents.weather_agent import weather_agent


app = FastAPI(title="ORCA Marine AI")


@app.get("/")
def home():
    return {
        "message": "ORCA Marine AI Backend is running"
    }


@app.post("/query", response_model=ORCAResponse)
def process_query(request: UserQuery):

    # 1. Run the Safety Agent
    safety_result = safety_agent(
        request.query,
        request.location
    )

    # 2. Get tool results
    tool_results = safety_result.get(
        "results",
        []
    )

    # 3. Summarize tool results
    summary = summarize_results(
        tool_results
    )

    # 4. Parse location
    latitude = None
    longitude = None

    if request.location:
        try:
            latitude, longitude = map(
                float,
                request.location.split(",")
            )
        except (ValueError, TypeError):
            pass

    # 5. Run Fishing Analytics Agent
    fishing_result = None

    if any(word in request.query.lower() for word in [
        "fish",
        "fishing",
        "pfz",
        "fishing zone",
        "potential fishing"
    ]):
        if latitude is not None and longitude is not None:
            fishing_result = fishing_agent(
                latitude,
                longitude
            )

    # 6. Run Weather Safety Agent
    weather_result = None

    if any(word in request.query.lower() for word in [
        "weather",
        "wind",
        "wave",
        "storm",
        "sea condition"
    ]):
        if latitude is not None and longitude is not None:
            weather_result = weather_agent(
                latitude,
                longitude
            )

    # 7. Add agent analyses to LLM context
    llm_context = summary.copy()

    if fishing_result:
        llm_context["fishing_analysis"] = fishing_result

    if weather_result:
        llm_context["weather_analysis"] = weather_result

    # 8. Generate answer
    answer = ask_llm(
        request.query,
        llm_context
    )

    # 9. Convert tool results into evidence
    evidence = []

    for result in tool_results:
        evidence.append({
            "source": result.get("source"),
            "tool": result.get("tool"),
            "status": result.get("status"),
            "data": result.get("data"),
            "message": result.get("message")
        })

    # 10. Add fishing analysis as evidence
    if fishing_result:
        evidence.append({
            "source": fishing_result.get(
                "source",
                "ORCA Fishing Analytics Agent"
            ),
            "tool": "fishing_analysis",
            "status": fishing_result.get(
                "suitability",
                "UNKNOWN"
            ),
            "data": fishing_result,
            "message": (
                "Fishing suitability analysis generated "
                "from mock ocean data."
            )
        })

    # 11. Add weather analysis as evidence
    if weather_result:
        evidence.append({
            "source": weather_result.get(
                "source",
                "ORCA Weather Safety Agent"
            ),
            "tool": "weather_analysis",
            "status": weather_result.get(
                "assessment",
                "UNKNOWN"
            ),
            "data": weather_result,
            "message": (
                "Weather condition assessment generated "
                "from mock weather data."
            )
        })

    # 12. Return structured ORCA response
    return ORCAResponse(
        query=request.query,
        location=request.location,
        language=request.language,
        user_type=request.user_type,

        agent={
            "name": safety_result.get(
                "agent",
                "Safety Agent"
            ),
            "tools_used": safety_result.get(
                "tools_selected",
                []
            )
        },

        answer=answer,

        safety=safety_result.get(
            "safety"
        ),

        evidence=evidence
    )