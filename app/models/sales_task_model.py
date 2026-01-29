from sqlalchemy import Column, Integer, Date, String, ForeignKey
from database.db_base import Base

class SalesTask(Base):
    __tablename__ = "sales_tasks"

    id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    goal_description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, default="pending")
