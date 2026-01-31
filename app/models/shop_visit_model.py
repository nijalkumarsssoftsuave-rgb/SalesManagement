from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey,Float
from database.db_base import Base


class ShopVisit(Base):
    __tablename__ = "shop_visits"

    id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer)
    product_id = Column(Integer)
    shop_name = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    distance_km = Column(Float)
    travel_time_min = Column(Integer)
    status = Column(String)  # ACCEPTED / REJECTED / HOLD
    visit_date = Column(Date)
