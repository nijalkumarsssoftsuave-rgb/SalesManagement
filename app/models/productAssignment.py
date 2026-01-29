# from sqlalchemy import Column, Integer, ForeignKey,UniqueConstraint
# from sqlalchemy.orm import relationship
# from database.db_base import Base
#
#
# class ProductAssignment(Base):
#     __tablename__ = "product_assignments"
#
#     id = Column(Integer, primary_key=True, index=True)
#
#     product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
#     teammember_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#
#     assigned_quantity = Column(Integer, nullable=False)
#
#     product = relationship("Product", back_populates="assignments")
#     teammember = relationship("User", back_populates="assigned_products")
#
#     __table_args__ = (
#         UniqueConstraint("product_id", "teammember_id", name="unique_product_teammember"),
#     )

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.db_base import Base


class ProductAssignment(Base):
    __tablename__ = "product_assignments"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    teammember_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    assigned_quantity = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="assignments")
    teammember = relationship("User", back_populates="assigned_products")

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "teammember_id",
            name="unique_product_teammember"
        ),
    )
