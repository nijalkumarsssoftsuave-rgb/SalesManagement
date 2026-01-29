from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.productAssignment import ProductAssignment
from app.models.users_model import User
from app.models.team_request_model import TeamRequest



def get_my_team_service(db: Session, manager_id: int):
    rows = (
        db.query(
            User.id.label("user_id"),
            User.name.label("user_name"),
            ProductAssignment.product_id,
            ProductAssignment.assigned_quantity
        )
        .join(
            ProductAssignment,
            ProductAssignment.teammember_id == User.id,
            isouter=True  # include members even if no products assigned
        )
        .filter(User.manager_id == manager_id)
        .all()
    )

    return [
        {
            "id": r.user_id,
            "name": r.user_name,
            "product_id": r.product_id,
            "quantity": r.assigned_quantity
        }
        for r in rows
    ]


def change_team_member_manager_service(
    db: Session,
    member_id: int,
    new_manager_id: int,
    current_manager_id: int
):
    member = db.query(User).filter(
        User.id == member_id,
        User.manager_id == current_manager_id
    ).first()

    if not member:
        raise HTTPException(404, "Team member not found")

    new_manager = db.query(User).filter(
        User.id == new_manager_id,
        User.role == "manager"
    ).first()

    if not new_manager:
        raise HTTPException(404, "Target manager not found")

    member.manager_id = new_manager_id
    db.commit()

    return {"message": "Team member reassigned"}


def request_team_member_service(db: Session, member_id: int, manager_id: int):
    existing = db.query(TeamRequest).filter(
        TeamRequest.member_id == member_id,
        TeamRequest.status == "pending"
    ).first()

    if existing:
        raise HTTPException(400, "Request already pending")

    req = TeamRequest(
        member_id=member_id,
        requested_by_manager_id=manager_id,
        status="pending"
    )

    db.add(req)
    db.commit()

    return {"message": "Team member request sent"}
