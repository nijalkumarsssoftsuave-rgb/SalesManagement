from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.security.rbac import require_min_role
from app.constants.roles import ROLE_TEAM
from database.sqllite_engine import get_db

from app.ai.intent_parser import parse_intent
from app.maps.product_place_mapper import get_place_types_for_product
from app.maps.places_service import find_places_nearby
from app.service.map_route_service import build_optimized_route

salesman_router = APIRouter(prefix="/salesman/ai", tags=["Salesman AI"])


@salesman_router.post("/sell-plan")
def generate_sell_plan(
    query: str,
    lat: float,
    lng: float,
    db: Session = Depends(get_db),
    user=Depends(require_min_role(ROLE_TEAM))
):
    intent = parse_intent(query)

    product = intent.get("product")
    radius_km = intent.get("radius_km", 50)

    place_types = get_place_types_for_product(product)

    places = find_places_nearby(
        lat, lng,
        place_types,
        radius_meters=radius_km * 1000
    )

    route = build_optimized_route(lat, lng, places[:10])  # LIMIT = cost control

    return {
        "product": product,
        "places": places[:10],
        "optimized_route": route
    }
