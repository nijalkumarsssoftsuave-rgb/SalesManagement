from fastapi import FastAPI
from contextlib import asynccontextmanager


from app.routes.auth_routes import auth_router
from database.db_base import Base
from database.sqllite_engine import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)   # DEV only
    yield
    # Shutdown
    # (cleanup if needed)

app = FastAPI(
    title="Sales Management System",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}