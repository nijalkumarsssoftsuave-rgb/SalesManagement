from  sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from database.db_base import Base
from datetime import datetime

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # user | assistant
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
