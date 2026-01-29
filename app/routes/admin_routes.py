from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database.sqllite_engine import get_db
from app.security.rbac import require_min_role
from app.models.users_model import User
from app.pydantics.signup_pydantic import ManagerCreate, TeamMemberCreate
from app.service.user_service import create_manager, create_team_member
from app.service.admin_services import (
    get_all_managers_service,
    get_managers_with_teams_service,
    handle_team_request_service
)
from app.service.product_services import get_all_products_service

admin_router = APIRouter(prefix="/admin" , tags=["Admin"])

@admin_router.post(
    "/admin/create-manager",
    dependencies=[Depends(require_min_role("ADMIN"))]
)
def admin_create_manager(
    data: ManagerCreate,
    db: Session = Depends(get_db)
):
    return create_manager(db, data)

@admin_router.get("/admin/managers")
def get_all_managers(
    db: Session = Depends(get_db),
    current_user=Depends(require_min_role("ADMIN"))
):
    return get_all_managers_service(db)

@admin_router.get("/admin/managers/teams")
def get_managers_with_teams(
    db: Session = Depends(get_db),
    current_user=Depends(require_min_role("ADMIN"))
):
    return get_managers_with_teams_service(db)

@admin_router.put("/team-request/{request_id}")
def handle_team_request(
    request_id: int,
    approve: bool,
    db: Session = Depends(get_db),
    current_user=Depends(require_min_role("admin"))
):
    return handle_team_request_service(db, request_id, approve)

@admin_router.get("/admin/all", dependencies=[Depends(require_min_role("ADMIN"))])
def view_all_products(db: Session = Depends(get_db)):
    return get_all_products_service(db)

