from app.tools.weather_tools import get_weather


def weather_agent(
    latitude: float,
    longitude: float
) -> dict:

    weather = get_weather(
        latitude,
        longitude
    )

    if weather.status != "AVAILABLE":
        return {
            "agent": "Weather Safety Agent",
            "status": "DATA_UNAVAILABLE",
            "assessment": "UNKNOWN",
            "source": weather.source,
            "factors": {}
        }

    data = weather.data

    wind_speed = data["wind_speed"]
    wave_height = data["wave_height"]

    # Prototype safety thresholds
    if wind_speed <= 25 and wave_height <= 1.5:
        assessment = "ACCEPTABLE"
    elif wind_speed <= 40 and wave_height <= 2.5:
        assessment = "CAUTION"
    else:
        assessment = "DANGEROUS"

    return {
        "agent": "Weather Safety Agent",
        "status": "AVAILABLE",
        "assessment": assessment,
        "factors": {
            "wind_speed_kmh": wind_speed,
            "wave_height_m": wave_height,
            "weather_condition": data["weather_condition"]
        },
        "source": weather.source,
        "message": "Weather condition assessment generated from Open-Meteo data."
    }
