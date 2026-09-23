def evaluate_safety(tool_results: list[dict]) -> dict:
    """
    Deterministic safety evaluation.
    Safety decisions are based on tool results, not the LLM.
    """

    alerts = []

    for result in tool_results:
        tool = result.get("tool")
        status = result.get("status")

        if tool == "geofence":
            if status == "RESTRICTED":
                alerts.append({
                    "level": "CRITICAL",
                    "type": "BOUNDARY_VIOLATION",
                    "message": "Vessel is inside a restricted marine zone."
                })

            elif status == "APPROACHING":
                alerts.append({
                    "level": "WARNING",
                    "type": "BOUNDARY_APPROACH",
                    "message": "Vessel is approaching a restricted marine zone."
                })

    if any(alert["level"] == "CRITICAL" for alert in alerts):
        overall_status = "CRITICAL"
    elif alerts:
        overall_status = "WARNING"
    else:
        overall_status = "SAFE"

    return {
        "overall_status": overall_status,
        "alerts": alerts
    }