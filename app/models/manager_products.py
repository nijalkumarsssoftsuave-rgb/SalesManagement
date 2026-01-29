# # app/models/manager_product.py
# from sqlalchemy import Column, Integer, ForeignKey, DateTime
# from datetime import datetime
# from database.db_base import Base
#
# class ManagerProduct(Base):
#     __tablename__ = "manager_products"
#
#     id = Column(Integer, primary_key=True)
#
#     manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
#
#     task_assigned_date = Column(DateTime, default=datetime.utcnow)
#     no_of_teammembers = Column(Integer, default=0)

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from database.db_base import Base


class ManagerProduct(Base):
    __tablename__ = "manager_products"

    id = Column(Integer, primary_key=True)

    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    task_assigned_date = Column(DateTime, default=datetime.utcnow)
    no_of_teammembers = Column(Integer, default=0)
