from app.models.tool_result import ToolResult


def get_sst(latitude: float, longitude: float) -> ToolResult:
    return ToolResult(
        tool="sst",
        status="AVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude,
            "value": 28.4,
            "unit": "°C",
            "timestamp": "2026-09-24T00:00:00Z"
        },
        message="Mock sea surface temperature data retrieved.",
        source="ORCA Mock Ocean Data"
    )


def get_chlorophyll(latitude: float, longitude: float) -> ToolResult:
    return ToolResult(
        tool="chlorophyll",
        status="AVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude,
            "value": 0.72,
            "unit": "mg/m³",
            "timestamp": "2026-09-24T00:00:00Z"
        },
        message="Mock chlorophyll-a data retrieved.",
        source="ORCA Mock Ocean Data"
    )


def get_pfz(latitude: float, longitude: float) -> ToolResult:
    return ToolResult(
        tool="pfz",
        status="AVAILABLE",
        data={
            "latitude": latitude,
            "longitude": longitude,
            "confidence": 0.82,
            "classification": "HIGH",
            "timestamp": "2026-09-24T00:00:00Z"
        },
        message="Mock potential fishing zone data retrieved.",
        source="ORCA Mock Ocean Data"
    )
