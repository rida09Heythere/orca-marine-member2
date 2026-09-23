from app.models.tool_result import ToolResult


def get_weather(latitude: float, longitude: float) -> ToolResult:
    """
    Get marine weather conditions.

    Temporary development response.
    Member 3 will later connect this to a real weather/ocean data source.
    """

    return ToolResult(
        tool="weather",
        status="DATA_UNAVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude
        },
        message="Real weather data source is not connected yet.",
        source="ORCA development placeholder"
    )
