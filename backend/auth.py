from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET = "secret123"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(data):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=2)
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token