def summarize_results(results: list[dict]) -> dict:
    """
    Summarize tool results and identify unavailable data.
    """

    available = []
    unavailable = []
    errors = []

    for result in results:
        status = result.get("status")

        if status == "DATA_UNAVAILABLE":
            unavailable.append(result)

        elif status in ["TOOL_NOT_FOUND", "INVALID_LOCATION"]:
            errors.append(result)

        else:
            available.append(result)

    return {
        "available_results": available,
        "unavailable_results": unavailable,
        "errors": errors,
        "all_data_available": len(unavailable) == 0
    }
