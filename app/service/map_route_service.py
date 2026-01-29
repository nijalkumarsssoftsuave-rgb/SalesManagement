import requests
from app.maps.google_client import DIRECTIONS_URL, GOOGLE_API_KEY

def build_optimized_route(
    origin_lat: float,
    origin_lng: float,
    destinations: list
):
    if not destinations:
        return None

    waypoints = "|".join(
        [f"{d['lat']},{d['lng']}" for d in destinations]
    )

    params = {
        "key": GOOGLE_API_KEY,
        "origin": f"{origin_lat},{origin_lng}",
        "destination": f"{origin_lat},{origin_lng}",
        "waypoints": f"optimize:true|{waypoints}",
        "mode": "driving"
    }

    response = requests.get(DIRECTIONS_URL, params=params).json()
    route = response["routes"][0]

    return {
        "polyline": route["overview_polyline"]["points"],
        "distance_km": route["legs"][0]["distance"]["value"] / 1000,
        "duration_min": route["legs"][0]["duration"]["value"] / 60
    }
