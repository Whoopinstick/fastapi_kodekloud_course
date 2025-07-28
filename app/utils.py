# utilities and helper functions
from passlib.context import CryptContext

# add this to work around an error with passlib and the latest bcrypt
# AttributeError: module 'bcrypt' has no attribute '__about__'
import logging
logging.getLogger('passlib').setLevel(logging.ERROR)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

