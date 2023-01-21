from passlib.context import CryptContext

# To encrypt the password
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def get_hashed_password(password: str):
