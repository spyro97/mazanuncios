from passlib.context import CryptContext
from models.user import User
from datetime import datetime, timedelta
from utils.const import (
    JWT_EXPIRATION_TIME_MINUTES,
    JWT_ALGORITH,
    JWT_SECRET_KEY,
    JWT_EXPIRED_MSG,
    JWT_INVALID_MSG,
    JWT_WRONG_ROLE,
)
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import time
from utils.db_functions import db_check_token_user, db_check_jwt_username
from starlette.status import HTTP_401_UNAUTHORIZED


pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# Authenticate username and password to give JWT token
async def authenticate_user(user: User):
    db_user = await db_check_token_user(user)
    if user:
        if verify_password(user.password, db_user['password']):
            return db_user
    else:
        return None


# Create access JWT token
def create_jwt_token(user: User):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"user": user['username'], "role": user['role'], "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITH)

    return jwt_token


# Check whether JWT token is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITH)
        username = jwt_payload.get("user")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                return final_checks(role)
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail=JWT_INVALID_MSG
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=JWT_EXPIRED_MSG
            )
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=JWT_WRONG_ROLE)
