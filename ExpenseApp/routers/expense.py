from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from ..model import ExpenseCreate, ExpenseRead, Expense, User
from ..database import get_session
from sqlmodel import Session
from ..database import engine
from ..auth_bearer import JWTBearer
from sqlmodel import Session


# Routers for user API
router = APIRouter(
    prefix="/v1",
    tags=["Expense"],
)


@router.post(
    "/expense/",
    response_model=ExpenseRead,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
# Hero create model is passed as argument to add the data
def create_expense(
    *,
    session: Session = Depends(get_session),
    expense: ExpenseCreate,
    request: Request,
    current_user_jwt: User = Depends(JWTBearer()),
):
    #   with Session(engine) as session:
    # Creating a new expense entry in database using Expense datatable
    new_expense = Expense.from_orm(expense)
    # print(f"new_expense: {new_expense}")
    if new_expense.description == "":
        raise HTTPException(status_code=422, detail="Description is required")
    print(new_expense.amount)
    if new_expense.amount == 0 or new_expense.amount == None:
        raise HTTPException(status_code=422, detail="Amount must should not be zero")
    if new_expense.date == "":
        raise HTTPException(status_code=422, detail="Date is required")

    current_active_username = JWTBearer().get_username(current_user_jwt)
    current_user_object = (
        session.query(User).filter(User.username == current_active_username).first()
    )
    print(f"Current_User_id in expense: {current_user_object.id}")
    # new_expense['creator_id'] = current_user_object.id
    new_expense.creator_id = current_user_object.id
    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)
    return new_expense


@router.get("/expense_get/", response_model=ExpenseRead)
def get_expense_by_user(*, session: Session = Depends(get_session), email: str):
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
