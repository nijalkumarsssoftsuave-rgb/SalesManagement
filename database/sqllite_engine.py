import os
from fastapi import HTTPException
from sqlalchemy import create_engine, false
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
load_dotenv()

DATABASE_URI =os.getenv("DATABASE_URL")

if not DATABASE_URI:
    raise RuntimeError("DATABASE_URI not set")

engine = create_engine(
    DATABASE_URI,
)

SessionLocal= sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
