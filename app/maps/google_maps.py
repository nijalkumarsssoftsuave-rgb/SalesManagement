from dotenv import load_dotenv
import requests
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_address(address: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}
    res = requests.get(url, params=params).json()

    location = res["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]


def nearby_places(lat, lng, radius=50000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "electronics_store",
        "key": GOOGLE_API_KEY
    }
    res = requests.get(url, params=params).json()
    return res.get("results", [])[:10]
