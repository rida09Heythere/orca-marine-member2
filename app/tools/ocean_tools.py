from app.models.tool_result import ToolResult


def get_sst(latitude: float, longitude: float) -> ToolResult:
    """
    Get Sea Surface Temperature.

    Temporary development response.
    Member 3 will later connect this to real SST data.
    """

    return ToolResult(
        tool="sst",
        status="DATA_UNAVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude
        },
        message="Real SST data source is not connected yet.",
        source="ORCA development placeholder"
    )


def get_chlorophyll(latitude: float, longitude: float) -> ToolResult:
    """
    Get Chlorophyll-a concentration.

    Temporary development response.
    Member 3 will later connect this to real ocean data.
    """

    return ToolResult(
        tool="chlorophyll",
        status="DATA_UNAVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude
        },
        message="Real chlorophyll data source is not connected yet.",
        source="ORCA development placeholder"
    )


def get_pfz(latitude: float, longitude: float) -> ToolResult:
    """
    Get Potential Fishing Zone information.

    Temporary development response.
    """

    return ToolResult(
        tool="pfz",
        status="DATA_UNAVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude
        },
        message="Real PFZ data source is not connected yet.",
        source="ORCA development placeholder"
    )
