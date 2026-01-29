# app/models/product.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.db_base import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150), nullable=False)

    products_available = Column(Integer, default=0)

    product_created_time = Column(DateTime, default=datetime.utcnow)
