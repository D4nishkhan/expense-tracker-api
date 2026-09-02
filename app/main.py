"""FastAPI application entrypoint for the Expense Tracker API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import expenses

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A production-style Expense Tracker REST API built with FastAPI and SQLite.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router)


@app.get("/", tags=["root"])
def root():
    """Health check / welcome endpoint."""
    return {
        "message": "Welcome to the Expense Tracker API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }