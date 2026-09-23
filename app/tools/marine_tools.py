from app.tools.geofence import check_geofence
from app.tools.ocean_tools import (
    get_sst,
    get_chlorophyll,
    get_pfz
)
from app.tools.weather_tools import get_weather


def run_geofence(latitude: float, longitude: float):
    return check_geofence(latitude, longitude)


def get_marine_tools() -> dict:
    """
    Registry of tools available to ORCA.
    """

    return {
        "geofence": run_geofence,
        "sst": get_sst,
        "chlorophyll": get_chlorophyll,
        "pfz": get_pfz,
        "weather": get_weather
    }
