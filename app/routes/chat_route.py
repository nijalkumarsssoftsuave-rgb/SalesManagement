from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.sqllite_engine import get_db
from app.security.rbac import require_min_role
from app.constants.roles import ROLE_TEAM
from app.service.chat_service import unified_chat_service

chat_router = APIRouter(prefix="/chat", tags=["Unified Chat"])


@chat_router.post("/")
def chat(
    message: str,
    db: Session = Depends(get_db),
    user=Depends(require_min_role(ROLE_TEAM))
):
    return unified_chat_service(db, user, message)