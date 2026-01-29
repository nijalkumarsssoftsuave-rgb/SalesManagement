# app/models/sold_products.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from database.db_base import Base

class SoldProduct(Base):
    __tablename__ = "sold_products"

    id = Column(Integer, primary_key=True)

    team_member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    quantity_sold = Column(Integer, nullable=False)

    sold_at = Column(DateTime, default=datetime.now)
