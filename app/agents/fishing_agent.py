from app.tools.ocean_tools import (
    get_sst,
    get_chlorophyll,
    get_pfz
)


def fishing_agent(
    latitude: float,
    longitude: float
) -> dict:

    sst = get_sst(latitude, longitude)
    chlorophyll = get_chlorophyll(latitude, longitude)
    pfz = get_pfz(latitude, longitude)

    sst_value = sst.data["value"]
    chlorophyll_value = chlorophyll.data["value"]
    pfz_confidence = pfz.data["confidence"]

    score = 0

    # Mock prototype reasoning rules
    if 24 <= sst_value <= 30:
        score += 1

    if chlorophyll_value >= 0.5:
        score += 1

    if pfz_confidence >= 0.7:
        score += 1

    if score == 3:
        suitability = "HIGH"
    elif score == 2:
        suitability = "MODERATE"
    else:
        suitability = "LOW"

    return {
        "agent": "Fishing Analytics Agent",
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "suitability": suitability,
        "score": score,
        "max_score": 3,
        "factors": {
            "sst_c": sst_value,
            "chlorophyll_mg_m3": chlorophyll_value,
            "pfz_confidence": pfz_confidence
        },
        "source": "ORCA Mock Ocean Data"
    }
