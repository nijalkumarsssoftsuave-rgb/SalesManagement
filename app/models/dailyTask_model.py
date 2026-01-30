from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database.db_base import Base
# app/models/daily_task.py
class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    total_quantity = Column(Integer)
    target_per_person = Column(Integer)
    task_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
