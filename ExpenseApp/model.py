from typing import Optional

# One line of FastAPI imports here later 👈
from sqlmodel import Field, Session, SQLModel, create_engine, select

import uuid as uuid_pkg


class UserBase(SQLModel):
    username: str = Field(index=True, description="to give a name")
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
