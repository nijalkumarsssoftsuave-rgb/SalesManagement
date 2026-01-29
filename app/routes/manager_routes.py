from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security.rbac import require_min_role
from database.sqllite_engine import get_db
from app.service.manager_services import (change_team_member_manager_service,
                                          request_team_member_service,
                                          get_my_team_service,
                                          )
from app.service.product_services import (create_product_service,
                                          update_product_quantity_service,
                                          get_manager_products_service,
                                          assign_product_service)
from app.security.dependencies import get_current_user
from app.pydantics.product_pydantics import ProductCreate

manager_router = APIRouter(prefix="/manager", tags=["manager"])


@manager_router.get("/team")
def get_my_team(
    db: Session = Depends(get_db),
    current_user=Depends(require_min_role("MANAGER"))
):
    return get_my_team_service(db, current_user["id"])

@manager_router.put("/team/change-manager/{member_id}")
def change_team_member_manager(
    member_id: int,
    new_manager_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_min_role("MANAGER"))
):
    return change_team_member_manager_service(
        db,
        member_id,
        new_manager_id,
        current_user["id"]
    )

@manager_router.post("/request-member/{member_id}")
def request_team_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_min_role("MANAGER"))
):
    return request_team_member_service(db, member_id, current_user["id"])

@manager_router.post("/")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_min_role("MANAGER"))
):
    return create_product_service(db, user, data)


@manager_router.put("/{product_id}/quantity")
def update_quantity(
    product_id: int,
    qty: int,
    db: Session = Depends(get_db),
    user=Depends(require_min_role("MANAGER"))
):
    return update_product_quantity_service(db, user, product_id, qty)


@manager_router.get("/manager/my-products")
def manager_products(
    db: Session = Depends(get_db),
    user=Depends(require_min_role("MANAGER"))
):
    return get_manager_products_service(db, user)


@manager_router.post("/{product_id}/assign")
def assign_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_min_role("MANAGER"))
):
    return assign_product_service(db, user, product_id)
