from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..model import UserCreate, UserRead, User, Login
from sqlmodel import Session, SQLModel, select
from ..database import engine
from ..hashing import verify_password

# Routers for user API
router = APIRouter(
    prefix="/v1",
    tags=["Login"],
)

# Providing a session to use it in the function instead of defining one by one
def get_session():
    with Session(engine) as session:
        yield session


@router.post("/login", response_model=UserRead, status_code=201)
async def login(*, session: Session = Depends(get_session), login: Login):
    user = session.query(User).filter(User.username == login.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid username and password")
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid username and password")
    # Generate a JWT token
    return user


# @router.post("/login", response_model=UserRead, status_code=201)
# # User create model is passed as argument to add the data
# def create_user(*, session: Session = Depends(get_session), user: UserCreate):
#     # with Session(engine) as session:
#     # Hashing a password
#     # hashedPassword = pwd_cxt.hash(user.password)
#     # User is called from the ORM
#     new_user = User(
#         username=user.username,
#         email=user.email,
#         password=get_hashed_password(user.password),
#     )
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
#     return new_user
