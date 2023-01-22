from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


# Creating tables in the database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Providing a session to use it in the function instead of defining one by one
def get_session():
    with Session(engine) as session:
        yield session
