from app.models.productAssignment import ProductAssignment
from app.models.product_model import Product
from app.models.dailyTask_model import DailyTask
from app.models.users_model import User
from datetime import date
from sqlalchemy.orm import Session
from app.models.shop_visit_model import ShopVisit
from sqlalchemy import func

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

# app/service/salesman_task_service.py
# def get_today_task(db, salesman_id):
#     return db.query(SalesmanTask).filter(
#         SalesmanTask.salesman_id == salesman_id,
#         SalesmanTask.task_date == date.today()
#     ).all()


def get_today_task_for_salesman(db: Session, user: dict):
    # find manager
    salesman = db.query(User).filter(User.id == user["id"]).first()
    if not salesman or not salesman.manager_id:
        return {"message": "No manager assigned"}

    task = db.query(DailyTask).filter(
        DailyTask.manager_id == salesman.manager_id,
        DailyTask.task_date == date.today()
    ).first()

    if not task:
        return {"message": "No task assigned for today"}

    # split quantity equally
    team_count = db.query(User).filter(
        User.manager_id == salesman.manager_id
    ).count()

    per_person_qty = task.total_quantity // max(team_count, 1)

    return {
        "product": task.product_name,
        "total_quantity": task.total_quantity,
        "your_quantity": per_person_qty,
        "target_per_person": task.target_per_person
    }



def handle_salesman_task(db, user):
    manager_id = user.get("manager_id")

    # Salesman without manager
    if not manager_id:
        return {
            "message": "No manager assigned to you. Please contact admin."
        }

    # Fetch today's task
    task = db.query(DailyTask).filter(
        DailyTask.manager_id == manager_id,
        DailyTask.task_date == date.today()
    ).first()

    # ✅ HANDLE NO TASK UPDATED
    if not task:
        return {
            "message": "No task has been updated for today by your manager."
        }

    # Count team members under this manager
    team_count = db.query(User).filter(
        User.manager_id == manager_id
    ).count()

    if team_count == 0:
        return {
            "message": "No team members found under your manager."
        }

    per_person_qty = task.total_quantity // team_count

    return {
        "mode": "SALESMAN_TASK",
        "product_id": task.product_id,
        "quantity": per_person_qty,
        "target": task.target_per_person
    }

# def salesman_analytics(db: Session, salesman_id: int):
#     visits = db.query(ShopVisit).filter(
#         ShopVisit.salesman_id == salesman_id
#     ).all()
#
#     return {
#         "total_shops": len(visits),
#         "accepted": sum(v.status == "ACCEPTED" for v in visits),
#         "rejected": sum(v.status == "REJECTED" for v in visits),
#         "hold": sum(v.status == "HOLD" for v in visits)
#     }


def get_salesman_daily_analytics(db, salesman_id):
    stats = db.query(
        ShopVisit.status,
        func.count(ShopVisit.id)
    ).filter(
        ShopVisit.salesman_id == salesman_id,
        ShopVisit.visit_date == date.today()
    ).group_by(ShopVisit.status).all()

    summary = {status: count for status, count in stats}

    return {
        "date": str(date.today()),
        "accepted": summary.get("ACCEPTED", 0),
        "rejected": summary.get("REJECTED", 0),
        "hold": summary.get("HOLD", 0)
    }