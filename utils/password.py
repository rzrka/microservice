from passlib.context import CryptContext
from sqlalchemy.util import deprecated

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def get_password_hash(password: str) ->str:
    return pwd_context.hash(password)