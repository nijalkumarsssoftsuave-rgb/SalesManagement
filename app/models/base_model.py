from database.db_base import Base
from sqlalchemy import Column,DateTime,func
from datetime import datetime


def created_at_column():
    return Column(DateTime,default=datetime.now,nullable=False)

def updated_at_column():
    return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

