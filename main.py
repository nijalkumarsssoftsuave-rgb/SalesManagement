from fastapi import FastAPI
from contextlib import asynccontextmanager
import app.models
from app.routes.admin_routes import admin_router
from app.routes.auth_routes import auth_router
from app.routes.manager_routes import manager_router
from database.db_base import Base
from database.sqllite_engine import engine
from app.routes.salesman_chat_routes import salesman_chat
from app.routes.salesman_ai_route import salesman_router
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
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(salesman_chat)
app.include_router(salesman_router)
# app.include_router(loca)

@app.get("/health")
def health_check():
    return {"status": "ok"}