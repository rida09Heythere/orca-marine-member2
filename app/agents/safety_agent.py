from app.tools.marine_tools import run_geofence


def safety_agent(query: str, location: str | None = None) -> dict:
    """
    Decide whether the query requires a marine safety/geofence check.
    """

    safety_keywords = [
        "safe",
        "safety",
        "border",
        "boundary",
        "restricted",
        "zone",
        "eez",
        "imbl",
        "near",
        "fishing"
    ]

    needs_geofence = any(
        keyword in query.lower()
        for keyword in safety_keywords
    )

    if not needs_geofence:
        return {
            "tool_used": None,
            "result": None
        }

    if not location:
        return {
            "tool_used": "geofence",
            "result": {
                "status": "LOCATION_REQUIRED",
                "message": "A latitude and longitude are required for a geofence safety check."
            }
        }

    try:
        latitude, longitude = map(
            float,
            location.split(",")
        )

        result = run_geofence(latitude, longitude)

        return {
            "tool_used": "geofence",
            "result": result.model_dump()
        }

    except (ValueError, TypeError):
        return {
            "tool_used": "geofence",
            "result": {
                "status": "INVALID_LOCATION",
                "message": "Location must be in 'latitude, longitude' format."
            }
        }
