from typing import Optional, List

# One line of FastAPI imports here later 👈
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from pydantic import EmailStr, validator
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime

import uuid as uuid_pkg


class UserBase(SQLModel):
    username: str = Field(index=True, description="to give a name", unique=True)
    email: str = Field(index=True, description="to give an email")


# Inheriting the base model for user and adding id class
# before using SQL Alchemy to create model in database
class User(UserBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    password: str
    # expenses: List["Expense"] = Relationship(back_populates="user")


# To create a user in a database
class UserCreate(UserBase):
    password: str
    pass


# To read a user from a database
class UserRead(UserBase):
    id: uuid_pkg.UUID


# To login in the system
class Login(SQLModel):
    username: str
    password: str


# to generate the token for our end point
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


# to create a expense in database


class ExpenseBase(SQLModel):
    amount: int = Field(nullable=False)
    description: Optional[str] = Field(default=None, index=True)
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Expense(ExpenseBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    creator_id: Optional[uuid_pkg.UUID] = Field(default=None, foreign_key="user.id")


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: uuid_pkg.UUID
