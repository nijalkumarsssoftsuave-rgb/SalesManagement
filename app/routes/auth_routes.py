from typing import Union
from app.pydantics.auth_pydantic import LoginRequest, TokenResponse, ChangePasswordRequest, PasswordChangeRequiredResponse
from app.service.auth_service import login_user, change_password_first_login_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.sqllite_engine import get_db
from app.pydantics.signup_pydantic import ManagerCreate, TeamMemberCreate
from app.service.user_service import create_manager, create_team_member
from app.security.dependencies import get_current_user
from app.security.rbac import require_min_role
from app.security.dependencies import get_password_reset_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login",
                  response_model=Union[
                      TokenResponse,
                      PasswordChangeRequiredResponse
                  ])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)

@auth_router.post("/change-password-first-login")
def change_password_first_login(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    reset_user = Depends(get_password_reset_user)
):
    change_password_first_login_service(
        db=db,
        user_id=reset_user["id"],
        old_password=data.old_password,
        new_password=data.new_password
    )
    return {
        "message": "Password updated successfully. Please login again."
    }



@auth_router.post(
    "/manager/create-team-member",
    dependencies=[Depends(require_min_role("MANAGER"))]
)
def manager_create_team_member(
    data: TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_team_member(db, data, manager_id=current_user["id"])
