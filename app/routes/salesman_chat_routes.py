# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
#
# from database.sqllite_engine import get_db
# from app.security.rbac import require_min_role
# from app.constants.roles import ROLE_TEAM
# from app.ai.intent_parser import parse_intent
#
# chat_router = APIRouter(prefix="/salesman/chat", tags=["Salesman AI"])
#
# @chat_router.post("/")
# def salesman_chat(
#     query: str,
#     db: Session = Depends(get_db),
#     user=Depends(require_min_role(ROLE_TEAM))
# ):
#     intent = parse_intent(query)
#
#     return {
#         "parsed_intent": intent,
#         "message": "Intent parsed successfully"
#     }
