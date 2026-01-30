from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database.db_base import Base

class SalesmanTask(Base):
    __tablename__ = "salesman_tasks"

    id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer)
    quantity_assigned = Column(Integer)
    target = Column(Integer)
    task_date = Column(Date)
