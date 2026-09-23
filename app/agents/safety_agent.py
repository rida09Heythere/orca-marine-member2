from app.agents.tool_selector import select_tools
from app.agents.tool_executor import execute_tools
from app.agents.safety_guardrail import evaluate_safety


def safety_agent(
    query: str,
    location: str | None = None
) -> dict:

    selected_tools = select_tools(query)

    if not selected_tools:
        return {
            "agent": "Safety Agent",
            "tools_selected": [],
            "results": [],
            "safety": {
                "overall_status": "SAFE",
                "alerts": []
            }
        }

    latitude = None
    longitude = None

    if location:
        try:
            latitude, longitude = map(
                float,
                location.split(",")
            )
        except (ValueError, TypeError):
            return {
                "agent": "Safety Agent",
                "tools_selected": selected_tools,
                "results": [{
                    "status": "INVALID_LOCATION",
                    "message": (
                        "Location must be in "
                        "'latitude, longitude' format."
                    )
                }],
                "safety": {
                    "overall_status": "WARNING",
                    "alerts": []
                }
            }

    results = execute_tools(
        selected_tools,
        latitude,
        longitude
    )

    safety = evaluate_safety(results)

    return {
        "agent": "Safety Agent",
        "tools_selected": selected_tools,
        "results": results,
        "safety": safety
    }