from app.tools.marine_tools import get_marine_tools


def execute_tools(
    selected_tools: list[str],
    latitude: float | None = None,
    longitude: float | None = None
) -> list[dict]:
    """
    Execute the tools selected by the ORCA routing layer.
    """

    tools = get_marine_tools()
    results = []

    if latitude is None or longitude is None:
        for tool_name in selected_tools:
            results.append({
                "tool": tool_name,
                "status": "LOCATION_REQUIRED",
                "data": None,
                "message": "Latitude and longitude are required.",
                "source": None
            })

        return results

    for tool_name in selected_tools:

        tool = tools.get(tool_name)

        if tool is None:
            results.append({
                "tool": tool_name,
                "status": "TOOL_NOT_FOUND",
                "data": None,
                "message": "Requested tool is not registered.",
                "source": None
            })
            continue

        result = tool(latitude, longitude)

        results.append(result.model_dump())

    return results
