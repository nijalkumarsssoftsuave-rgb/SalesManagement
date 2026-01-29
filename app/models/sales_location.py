from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from database.db_base import Base

class SalesmanLocation(Base):
    __tablename__ = "salesman_locations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)
