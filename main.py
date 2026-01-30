from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

import app.models
from app.routes.admin_routes import admin_router
from app.routes.auth_routes import auth_router
from app.routes.manager_routes import manager_router
from database.db_base import Base
from database.sqllite_engine import engine
from app.routes.chat_route import chat_router
from app.routes.location_routes import location_router
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(chat_router)
app.include_router(salesman_router)
app.include_router(location_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}