from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.sqllite_engine import get_db
from app.security.rbac import require_min_role
from app.constants.roles import ROLE_TEAM
from app.service.chat_service import unified_chat_service
from app.pydantics.product_pydantics import DailyTaskRequest
from app.service.chat_service import save_daily_task

chat_router = APIRouter(prefix="/chat", tags=["Unified Chat"])


@chat_router.post("/")
def chat(
    message: str,
    db: Session = Depends(get_db),
    user=Depends(require_min_role(ROLE_TEAM))
):
    print(db)
    print(user)
    return unified_chat_service(db, user, message)


@chat_router.post("/daily")
def create_daily_task(request: DailyTaskRequest, db: Session = Depends(get_db)):
    try:
        save_daily_task(
            db=db,
            manager_id=request.manager_id,
            product_name=request.product_name,
            quantity=request.quantity,
            target=request.target
        )
        return {"message": "Daily task saved successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
