from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.users_model import User
from app.models.product_model import Product
from app.models.productAssignment import ProductAssignment
from app.pydantics.product_pydantics import ProductCreate
from app.constants.roles import ROLE_TEAM


def create_product_service(db: Session, user: dict, data: ProductCreate):
    product = Product(
        name=data.name,
        total_quantity=data.total_quantity,
        created_by=user["id"]
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product_quantity_service(db: Session, user: dict, product_id: int, qty: int):
    product = db.query(Product).filter_by(
        id=product_id,
        created_by=user["id"]
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.total_quantity += qty
    db.commit()
    db.refresh(product)
    return product


def get_all_products_service(db: Session):
    return db.query(Product).all()


def get_manager_products_service(db: Session, user: dict):
    return db.query(Product).filter_by(
        created_by=user["id"]
    ).all()

def assign_product_service(db: Session, user: dict, product_id: int):
    product = db.query(Product).filter_by(
        id=product_id,
        created_by=user["id"]
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    team_members = db.query(User).filter_by(
        manager_id=user["id"],
        role=ROLE_TEAM
    ).all()

    if not team_members:
        raise HTTPException(status_code=400, detail="No team members found")

    qty_per_member = product.total_quantity // len(team_members)

    assignments = []

    for member in team_members:
        existing = db.query(ProductAssignment).filter_by(
            product_id=product.id,
            teammember_id=member.id
        ).first()

        if existing:
            existing.assigned_quantity += qty_per_member
            assignments.append(existing)
        else:
            assignment = ProductAssignment(
                product_id=product.id,
                teammember_id=member.id,
                assigned_quantity=qty_per_member
            )
            db.add(assignment)
            assignments.append(assignment)

    db.commit()

    return [
        {
            "product_id": a.product_id,
            "teammember_id": a.teammember_id,
            "assigned_quantity": a.assigned_quantity
        }
        for a in assignments
    ]


# def assign_product_service(db: Session, user: dict, product_id: int):
#     product = db.query(Product).filter_by(
#         id=product_id,
#         created_by=user["id"]
#     ).first()
#
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#
#     team_members = db.query(User).filter_by(
#         manager_id=user["id"],
#         role=ROLE_TEAM
#     ).all()
#
#     if not team_members:
#         raise HTTPException(status_code=400, detail="No team members found")
#
#     qty_per_member = product.total_quantity // len(team_members)
#
#     assignments = []
#     for member in team_members:
#         assignment = ProductAssignment(
#             product_id=product.id,
#             teammember_id=member.id,
#             assigned_quantity=qty_per_member
#         )
#         db.add(assignment)
#         assignments.append(assignment)
#
#     db.commit()
#     return assignments


def get_teammember_products_service(db: Session, user: dict):
    return db.query(ProductAssignment).filter_by(
        teammember_id=user["id"]
    ).all()
