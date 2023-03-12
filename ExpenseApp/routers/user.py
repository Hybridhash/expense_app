from ..model import UserCreate, UserRead, User
from sqlmodel import Session, SQLModel, select
from ..database import engine
from ..hashing import get_hashed_password

# from ..jwt_token import get_current_user
from ..auth_bearer import JWTBearer
from fastapi import FastAPI, APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPBearer
import uuid as uuid_pkg
from typing import List
from pydantic import validator


# Routers for user API
router = APIRouter(
    prefix="/v1",
    tags=["User"],
)

# Providing a session to use it in the function instead of defining one by one
def get_session():
    with Session(engine) as session:
        yield session


@router.post("/user/", response_model=UserRead, status_code=201)
# User create model is passed as argument to add the data
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    # Hashing a password
    # hashedPassword = pwd_cxt.hash(user.password)
    # Validator to check that email and username already exist in database
    existing_email = session.query(User).filter(User.email == user.email).first()
    existing_username = session.query(User).filter(User.username == user.username).first()

    if existing_username:
        raise HTTPException(status_code=403, detail="Username not available")
    elif existing_email:
        raise HTTPException(status_code=403, detail="Email already exists")

    # User is called from the ORM
    new_user = User(
        username=user.username,
        email=user.email,
        password=get_hashed_password(user.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
