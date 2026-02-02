from sqlalchemy.orm import Session
from app.models.shop_visit_model import ShopVisit

def update_shop_status(db: Session, visit_id: int, status: str, user: dict):
    visit = db.query(ShopVisit).filter(
        ShopVisit.id == visit_id,
        ShopVisit.salesman_id == user["id"]
    ).first()

    if not visit:
        return {"message": "Visit not found"}

    visit.status = status
    db.commit()

    return {"message": f"Shop marked as {status}"}
