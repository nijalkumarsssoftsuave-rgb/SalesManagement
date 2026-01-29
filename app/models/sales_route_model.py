from sqlalchemy import Column, Integer, Date, Float, ForeignKey, Text
from database.db_base import Base

class SalesRoute(Base):
    __tablename__ = "sales_routes"

    id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    encoded_polyline = Column(Text, nullable=False)
    total_distance_km = Column(Float)
    total_duration_min = Column(Float)
