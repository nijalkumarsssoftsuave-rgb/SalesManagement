from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.sqllite_engine import get_db
from app.security.rbac import require_min_role
from app.constants.roles import ROLE_TEAM
from app.models.sales_location import SalesmanLocation

location_router = APIRouter(prefix="/salesman/location", tags=["Location"])

@location_router.post("/")
def update_location(
    lat: float,
    lng: float,
    db: Session = Depends(get_db),
    user=Depends(require_min_role(ROLE_TEAM))
):
    loc = SalesmanLocation(
        user_id=user["id"],
        latitude=lat,
        longitude=lng
    )
    db.add(loc)
    db.commit()

    return {"status": "location updated"}
