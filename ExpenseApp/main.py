from fastapi import FastAPI, HTTPException, APIRouter, Depends, Security
from sqlmodel import Session, SQLModel, select
from fastapi.security import HTTPBearer
from .database import create_db_and_tables
from .routers import user, auth, expense

app = FastAPI()

router = APIRouter(prefix="/v1", tags=["User"])

# Decorator to create the database tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Routers provided in the application
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(expense.router)
