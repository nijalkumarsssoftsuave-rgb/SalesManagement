from Tools.scripts.ptags import tags
from fastapi import APIRouter, Depends, HTTPException
from database.sqllite_engine import get_db
from sqlalchemy.orm import Session
from app.security.dependencies import get_current_user
from app.security.rbac import require_min_role
from app.service.product_services import get_teammember_products_service

team_router = APIRouter(prefix="/team", tags=["team"])

@team_router.get("/teammember/my-products", dependencies=[Depends(require_min_role("TEAM_MEMBER"))])
def team_products(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_teammember_products_service(db, user)
