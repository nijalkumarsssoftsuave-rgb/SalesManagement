from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.users_model import User
from app.security.password_hash import hash_password
from app.constants.roles import ROLE_MANAGER, ROLE_TEAM

def create_manager(db: Session, data):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    manager = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=ROLE_MANAGER,
        phone=data.phone,
        address=data.address
    )

    db.add(manager)
    db.commit()
    db.refresh(manager)
    return manager


def create_team_member(db: Session, data, manager_id: int):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    member = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=ROLE_TEAM,
        manager_id=manager_id
    )

    db.add(member)
    db.commit()
    db.refresh(member)
    return member
