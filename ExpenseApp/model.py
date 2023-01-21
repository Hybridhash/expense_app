from typing import Optional

# One line of FastAPI imports here later 👈
from sqlmodel import Field, Session, SQLModel, create_engine, select

import uuid as uuid_pkg


class UserBase(SQLModel):
    username: str = Field(index=True, description="to give a name")
    email: str = Field(index=True, description="to give an email")
    password: str


# Inheriting the base model for user and adding id class
# before using SQL Alchemy to create model in database
class User(UserBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


# To create a user in a database
class UserCreate(UserBase):
    pass


# To read a user from a database
class UserRead(UserBase):
    id: uuid_pkg.UUID
