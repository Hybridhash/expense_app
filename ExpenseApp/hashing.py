from passlib.context import CryptContext

# To encrypt the password
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing the password
def get_hashed_password(password: str):
    return pwd_cxt.hash(password)


# Verifying the password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_cxt.verify(plain_password, hashed_password)
