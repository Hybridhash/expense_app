from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..model import UserCreate, UserRead, User, Login
from sqlmodel import Session, SQLModel, select
from fastapi.security import OAuth2PasswordRequestForm
from ..database import engine
from ..hashing import verify_password

from ..jwt_token import create_access_token, access_token_expires


# Routers for user API
router = APIRouter(
    prefix="/v1",
    tags=["Login"],
)


# Providing a session to use it in the function instead of defining one by one
def get_session():
    with Session(engine) as session:
        yield session


@router.post("/login", status_code=201)
async def login(
    *,
    session: Session = Depends(get_session),
    login: Login,
):
    user = session.query(User).filter(User.username == login.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid username and password")
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid username and password")
    # Generate a JWT token

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Returning access token and type, there is no need for the response model now
    return {"access_token": access_token, "token_type": "bearer"}
