from sqlalchemy.orm import Session
from app.models.productAssignment import ProductAssignment
from app.models.product_model import Product

def get_assigned_products_for_salesman(db: Session, salesman_id: int):
    rows = (
        db.query(Product.id, Product.name, Product.category)
        .join(ProductAssignment, Product.id == ProductAssignment.product_id)
        .filter(ProductAssignment.teammember_id == salesman_id)
        .all()
    )

    return [
        {
            "product_id": r.id,
            "name": r.name,
            "category": r.category
        }
        for r in rows
    ]
