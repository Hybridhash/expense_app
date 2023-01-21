from ..model import UserCreate, UserRead, User
from sqlmodel import Session, SQLModel, select
from ..database import engine
from ..hashing import get_hashed_password
from fastapi import FastAPI, APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPBearer
import uuid as uuid_pkg
from typing import List


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
    # with Session(engine) as session:
    # Hashing a password
    # hashedPassword = pwd_cxt.hash(user.password)
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


# To get the user from the database based on email id
@router.get("/user/{user_id}", response_model=UserRead)
def read_user(*, session: Session = Depends(get_session), user_id: uuid_pkg.UUID):
    # with Session(engine) as session:
    hero = session.get(User, user_id)
    if not hero:
        raise HTTPException(status_code=404, detail="User not found")
    return hero


# To get the id for all users from database
@router.get("/users/", response_model=List[UserRead])
def read_heroes(
    *,
    session: Session = Depends(get_session),
):
    # with Session(engine) as session:
    # Hero model (in database) is called to select all records
    users = session.exec(select(User)).all()
    return users


# to get the user based on email id
@router.get("/users/{email}", response_model=UserRead)
def get_user_by_email(*, session: Session = Depends(get_session), email: str):
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
