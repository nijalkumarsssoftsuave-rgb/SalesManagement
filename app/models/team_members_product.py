from sqlalchemy import Column, Integer, DateTime, ForeignKey
from database.db_base import Base
from datetime import datetime


class TeamMemberProduct(Base):
    __tablename__ = "team_member_products"

    id = Column(Integer, primary_key=True)

    manager_product_id = Column(
        Integer,
        ForeignKey("manager_products.id"),
        nullable=False
    )
    team_member_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    products_assigned = Column(Integer, nullable=False)
    products_sold = Column(Integer, default=0)

    assigned_date = Column(DateTime, default=datetime.utcnow)
