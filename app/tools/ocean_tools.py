from app.models.tool_result import ToolResult
from app.tools.data_status import unavailable_data


def get_sst(latitude: float, longitude: float) -> ToolResult:
    return unavailable_data(
        "sst",
        latitude,
        longitude,
        "Real SST data source is not connected yet."
    )


def get_chlorophyll(latitude: float, longitude: float) -> ToolResult:
    return unavailable_data(
        "chlorophyll",
        latitude,
        longitude,
        "Real chlorophyll data source is not connected yet."
    )


def get_pfz(latitude: float, longitude: float) -> ToolResult:
    return unavailable_data(
        "pfz",
        latitude,
        longitude,
        "Real PFZ data source is not connected yet."
    )
