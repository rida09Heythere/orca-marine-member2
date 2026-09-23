def select_tools(query: str) -> list[str]:
    """
    Select relevant ORCA tools based on the user's query.

    This is a temporary deterministic selector.
    Later, Member 1's LangGraph/LLM routing can replace or extend it.
    """

    query_lower = query.lower()

    selected_tools = []

    if any(word in query_lower for word in [
        "border",
        "boundary",
        "restricted",
        "eez",
        "imbl",
        "near"
    ]):
        selected_tools.append("geofence")

    if any(word in query_lower for word in [
        "sst",
        "temperature",
        "sea temperature",
        "water temperature"
    ]):
        selected_tools.append("sst")

    if any(word in query_lower for word in [
        "chlorophyll",
        "chlorophyll-a",
        "chlorophyll a"
    ]):
        selected_tools.append("chlorophyll")

    if any(word in query_lower for word in [
        "fish",
        "fishing",
        "pfz",
        "fishing zone",
        "potential fishing"
    ]):
        selected_tools.append("pfz")

    if any(word in query_lower for word in [
        "weather",
        "wind",
        "wave",
        "storm",
        "rain",
        "forecast",
        "sea condition"
    ]):
        selected_tools.append("weather")

    return selected_tools
