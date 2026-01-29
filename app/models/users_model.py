# # app/models/user.py
# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database.db_base import Base
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#
#     name = Column(String(100), nullable=False)
#     email = Column(String(150), unique=True, nullable=False, index=True)
#     password = Column(String, nullable=False)
#
#     role = Column(String(20), nullable=False)
#     # ADMIN | MANAGER | TEAM_MEMBER
#
#     phone = Column(String(15))
#     address = Column(String)
#
#     manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
#     # NULL for ADMIN & MANAGER, set for TEAM_MEMBER
#
#     is_active = Column(Boolean, default=True)
#
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     must_change_password = Column(Boolean, default=False)
#
#     # Relationships
#     products = relationship("Product", back_populates="manager")
#     manager = relationship("User", remote_side=[id], backref="team_members")
#     assigned_products = relationship("ProductAssignment", back_populates="teammember", cascade="all, delete")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    role = Column(String(20), nullable=False)
    # ADMIN | MANAGER | TEAM_MEMBER

    phone = Column(String(15))
    address = Column(String)

    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    must_change_password = Column(Boolean, default=False)

    # Relationships
    products = relationship("Product", back_populates="manager")
    manager = relationship("User", remote_side=[id], backref="team_members")
    assigned_products = relationship(
        "ProductAssignment",
        back_populates="teammember",
        cascade="all, delete"
    )
