from shapely.geometry import Point, Polygon
from pyproj import Transformer


def check_geofence(latitude: float, longitude: float) -> dict:
    """
    Check vessel position against a restricted marine zone.

    NOTE:
    The polygon below is temporary test data.
    Member 3 will later provide the real GeoJSON boundaries.
    """

    restricted_zone = Polygon([
        (72.80, 18.80),
        (73.20, 18.80),
        (73.20, 19.20),
        (72.80, 19.20)
    ])

    vessel_position = Point(longitude, latitude)

    if restricted_zone.contains(vessel_position):
        return {
            "latitude": latitude,
            "longitude": longitude,
            "status": "RESTRICTED",
            "distance_to_boundary_m": 0,
            "message": "Vessel is inside the restricted zone."
        }

    # Convert geographic coordinates (WGS84) to Web Mercator meters.
    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3857",
        always_xy=True
    )

    vessel_x, vessel_y = transformer.transform(longitude, latitude)

    projected_boundary = []

    for lon, lat in restricted_zone.exterior.coords:
        x, y = transformer.transform(lon, lat)
        projected_boundary.append((x, y))

    projected_zone = Polygon(projected_boundary)

    distance_m = Point(vessel_x, vessel_y).distance(
        projected_zone.boundary
    )

    if distance_m < 5000:
        status = "APPROACHING"
        message = "Vessel is within 5 km of the restricted zone."
    else:
        status = "SAFE"
        message = "Vessel is outside the restricted zone."

    return {
        "latitude": latitude,
        "longitude": longitude,
        "status": status,
        "distance_to_boundary_m": round(distance_m, 2),
        "message": message
    }
