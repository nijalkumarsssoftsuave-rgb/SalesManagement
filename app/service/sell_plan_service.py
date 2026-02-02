from app.maps.google_maps import geocode_address, nearby_places
from sqlalchemy.orm import Session
from app.models.shop_visit_model import ShopVisit
from datetime import datetime, date

def update_shop_status(db: Session, visit_id: int, status: str, user: dict):
    visit = db.query(ShopVisit).filter(
        ShopVisit.id == visit_id,
        ShopVisit.salesman_id == user["id"]
    ).first()

    if not visit:
        return {"message": "Visit not found"}

    visit.status = status
    db.commit()

    return {"message": f"Shop marked as {status}"}

# def sell_plan_service(db, user, lat=None, lng=None, address=None):
#
#     if not lat or not lng:
#         if not address:
#             return {
#                 "message": "Location required. Please provide lat/lng or address."
#             }
#         lat, lng = geocode_address(address)
#
#     places = nearby_places(lat, lng)
#
#     shops = []
#     for p in places:
#         shop_lat = p["geometry"]["location"]["lat"]
#         shop_lng = p["geometry"]["location"]["lng"]
#
#         shops.append({
#             "place_id": p["place_id"],
#             "name": p["name"],
#             "lat": shop_lat,
#             "lng": shop_lng,
#             "map_url": f"https://www.google.com/maps?q={shop_lat},{shop_lng}"
#         })
#
#     return {
#         "current_location": {
#             "lat": lat,
#             "lng": lng,
#             "map_url": f"https://www.google.com/maps?q={lat},{lng}"
#         },
#         "shops": shops
#     }

def sell_plan_service(db, user, product_id, lat=None, lng=None, address=None):

    if not lat or not lng:
        if not address:
            return {"message": "Location required"}
        lat, lng = geocode_address(address)

    places = nearby_places(lat, lng)

    shops = []
    for p in places:
        shop_lat = p["geometry"]["location"]["lat"]
        shop_lng = p["geometry"]["location"]["lng"]

        # skip already visited shops
        visited = db.query(ShopVisit).filter(
            ShopVisit.salesman_id == user["id"],
            ShopVisit.shop_name == p["name"]
        ).first()

        if visited:
            continue

        visit = ShopVisit(
            salesman_id=user["id"],
            product_id=product_id,
            shop_name=p["name"],
            lat=shop_lat,
            lng=shop_lng,
            status="HOLD",
            visit_date=date.today()
        )

        db.add(visit)

        shops.append({
            "place_id": p["place_id"],
            "name": p["name"],
            "lat": shop_lat,
            "lng": shop_lng,
            "map_url": f"https://www.google.com/maps?q={shop_lat},{shop_lng}"
        })

    db.commit()

    return {
        "current_location": {
            "lat": lat,
            "lng": lng,
            "map_url": f"https://www.google.com/maps?q={lat},{lng}"
        },
        "shops": shops
    }