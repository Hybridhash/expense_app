from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from ..model import ExpenseCreate, ExpenseRead, Expense, User
from ..database import get_session
from sqlmodel import Session
from ..database import engine
from ..auth_bearer import JWTBearer
from sqlmodel import Session
from typing import List
import uuid as uuid_pkg


# Routers for user API
router = APIRouter(
    prefix="/v1",
    tags=["Transaction"],
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
    current_user_jwt: User = Depends(JWTBearer()),
):
    """Post Request:
    Post request to save new transaction for current active user"""
    # Creating a new expense entry in database using Expense datatable
    new_expense = Expense.from_orm(expense)
    # Input data is validated for missing value and validation errors are raised
    if new_expense.description == "":
        raise HTTPException(status_code=422, detail="Description is required")
    print(new_expense.amount)
    if new_expense.amount == 0 or new_expense.amount == None:
        raise HTTPException(status_code=422, detail="Amount must should not be zero")
    if new_expense.date == "":
        raise HTTPException(status_code=422, detail="Date is required")

    current_active_username = JWTBearer().get_username(current_user_jwt)
    current_user = session.query(User).filter(User.username == current_active_username).first()
    print(f"Current_User_id in expense: {current_user.id}")
    # Giving id for the creator on saving a new expense record.
    new_expense.creator_id = current_user.id
    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)
    return new_expense


@router.get("/get_transaction/", response_model=List[ExpenseRead])
def get_transaction_by_user(*, session: Session = Depends(get_session), current_user_jwt: User = Depends(JWTBearer())):
    """Get Request:
    Fetch the transaction for the user currently logged"""
    current_active_username = JWTBearer().get_username(current_user_jwt)
    current_user = session.query(User).filter(User.username == current_active_username).first()
    transactions = session.query(Expense).filter(Expense.creator_id == current_user.id).all()
    print(f"get_records_by_user in expense: {transactions}")
    if transactions is None:
        raise HTTPException(status_code=404, detail="No transaction found")
    return transactions


@router.delete("/delete_transaction/{transaction_id}")
def delete_transaction_by_id(
    transaction_id: uuid_pkg.UUID,
    session: Session = Depends(get_session),
    current_user_jwt: User = Depends(JWTBearer()),
):
    """Delete Request:
    Delete the transaction for the user currently logged based on transaction id"""
    current_active_username = JWTBearer().get_username(current_user_jwt)
    current_user = session.query(User).filter(User.username == current_active_username).first()
    transaction = session.query(Expense).filter(Expense.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"message": f"Transaction with id {transaction_id} deleted successfully"}
