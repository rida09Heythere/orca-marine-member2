from app.tools.geofence import check_geofence


def run_geofence(latitude: float, longitude: float) -> dict:
    """
    Run the marine geofence safety check.
    """
    return check_geofence(latitude, longitude)


def get_marine_tools() -> dict:
    """
    Registry of tools available to the ORCA agent.
    """

    return {
        "geofence": run_geofence
    }
