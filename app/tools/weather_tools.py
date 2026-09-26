import requests

from app.models.tool_result import ToolResult


def get_weather(latitude: float, longitude: float) -> ToolResult:

    marine_url = "https://marine-api.open-meteo.com/v1/marine"
    weather_url = "https://api.open-meteo.com/v1/forecast"

    marine_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "wave_height,"
            "wind_wave_height,"
            "swell_wave_height,"
            "sea_surface_temperature"
        )
    }

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "wind_speed_10m"
    }

    try:
        marine_response = requests.get(
            marine_url,
            params=marine_params,
            timeout=10
        )

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        marine_response.raise_for_status()
        weather_response.raise_for_status()

        marine_data = marine_response.json().get("current", {})
        weather_data = weather_response.json().get("current", {})

        wave_height = marine_data.get("wave_height")
        wind_speed = weather_data.get("wind_speed_10m")

        if wave_height is None or wind_speed is None:
            return ToolResult(
                tool="weather",
                status="DATA_UNAVAILABLE",
                data={
                    "latitude": latitude,
                    "longitude": longitude
                },
                message="Required marine/weather data unavailable.",
                source="Open-Meteo"
            )

        return ToolResult(
            tool="weather",
            status="AVAILABLE",
            data={
                "latitude": latitude,
                "longitude": longitude,
                "wind_speed": wind_speed,
                "wind_unit": "km/h",
                "wave_height": wave_height,
                "wave_unit": "m",
                "weather_condition": "Marine conditions available",
                "sea_surface_temperature": marine_data.get(
                    "sea_surface_temperature"
                ),
                "timestamp": marine_data.get("time")
            },
            message="Real marine and weather data retrieved.",
            source="Open-Meteo Marine + Weather API"
        )

    except Exception as e:

        return ToolResult(
            tool="weather",
            status="DATA_UNAVAILABLE",
            data={
                "latitude": latitude,
                "longitude": longitude
            },
            message=f"API request failed: {str(e)}",
            source="Open-Meteo"
        )
