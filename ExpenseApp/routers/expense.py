from fastapi import FastAPI, APIRouter, Depends
from ..model import ExpenseCreate, ExpenseRead, Expense
from ..database import get_session
from sqlmodel import Session
from ..database import engine

from sqlmodel import Session


# Routers for user API
router = APIRouter(
    prefix="/v1",
    tags=["Expense"],
)


@router.post("/expense/", response_model=ExpenseRead, status_code=201)
# Hero create model is passed as argument to add the data
def create_expense(*, session: Session = Depends(get_session), expense: ExpenseCreate):
    #   with Session(engine) as session:
    # Creating a new expense entry in database using Expense datatable
    new_expense = Expense.from_orm(expense)
    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)
    return new_expense
