from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.security.rbac import require_min_role
from app.constants.roles import ROLE_TEAM
from database.sqllite_engine import get_db
from app.service.sell_plan_service import sell_plan_service

salesman_router = APIRouter(prefix="/salesman/ai", tags=["Salesman AI"])

@salesman_router.post("/sell-plan")
def sell_plan(
    lat: float | None = None,
    lng: float | None = None,
    address: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_min_role(ROLE_TEAM))
):
    return sell_plan_service(db, user, lat, lng, address)