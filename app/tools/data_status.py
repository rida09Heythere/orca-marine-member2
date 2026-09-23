from app.models.tool_result import ToolResult


def unavailable_data(
    tool: str,
    latitude: float,
    longitude: float,
    message: str
) -> ToolResult:
    return ToolResult(
        tool=tool,
        status="DATA_UNAVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude
        },
        message=message,
        source="ORCA development placeholder"
    )

