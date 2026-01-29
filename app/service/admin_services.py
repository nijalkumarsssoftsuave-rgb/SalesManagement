from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.users_model import User
from app.models.team_request_model import TeamRequest


def get_all_managers_service(db: Session):
    return db.query(User).filter(User.role == "MANAGER").all()


def get_managers_with_teams_service(db: Session):
    managers = db.query(User).filter(User.role == "MANAGER").all()
    result = []

    for manager in managers:
        members = db.query(User).filter(
            User.manager_id == manager.id
        ).all()

        result.append({
            "manager_id": manager.id,
            "manager_name": manager.name,
            "team_members": members
        })

    return result


def handle_team_request_service(db: Session, request_id: int, approve: bool):
    req = db.query(TeamRequest).filter(
        TeamRequest.id == request_id
    ).first()

    if not req:
        raise HTTPException(404, "Request not found")

    if approve:
        member = db.query(User).filter(
            User.id == req.member_id
        ).first()

        member.manager_id = req.requested_by_manager_id
        req.status = "approved"
    else:
        req.status = "rejected"

    db.commit()
    return {"message": f"Request {req.status}"}
