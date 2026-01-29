import requests
from app.maps.google_client import PLACES_URL, GOOGLE_API_KEY

def find_places_nearby(
    lat: float,
    lng: float,
    place_types: list,
    radius_meters: int = 50000
):
    results = []

    for place_type in place_types:
        params = {
            "key": GOOGLE_API_KEY,
            "location": f"{lat},{lng}",
            "radius": radius_meters,
            "type": place_type
        }

        response = requests.get(PLACES_URL, params=params).json()

        for place in response.get("results", []):
            results.append({
                "name": place["name"],
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "address": place.get("vicinity")
            })

    return results
