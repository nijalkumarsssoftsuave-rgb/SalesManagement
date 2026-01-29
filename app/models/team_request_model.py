from sqlalchemy import Column, Integer, String, ForeignKey
from database.db_base import Base

class TeamRequest(Base):
    __tablename__ = "team_requests"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("users.id"))
    requested_by_manager_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
