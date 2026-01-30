from app.maps.google_maps import geocode_address, nearby_places

def sell_plan_service(db, user, lat=None, lng=None, address=None):

    if not lat or not lng:
        if not address:
            return {
                "message": "Location required. Please provide lat/lng or address."
            }
        lat, lng = geocode_address(address)

    places = nearby_places(lat, lng)

    shops = []
    for p in places:
        shop_lat = p["geometry"]["location"]["lat"]
        shop_lng = p["geometry"]["location"]["lng"]

        shops.append({
            "place_id": p["place_id"],
            "name": p["name"],
            "lat": shop_lat,
            "lng": shop_lng,
            "map_url": f"https://www.google.com/maps?q={shop_lat},{shop_lng}"
        })

    return {
        "current_location": {
            "lat": lat,
            "lng": lng,
            "map_url": f"https://www.google.com/maps?q={lat},{lng}"
        },
        "shops": shops
    }
