from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db_base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_quantity = Column(Integer, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # category = Column(String, nullable=False)

    manager = relationship("User", back_populates="products")
    assignments = relationship(
        "ProductAssignment",
        back_populates="product",
        cascade="all, delete"
    )
