from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from requests import Session

from models.user_model import UserModel

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 200
SECRET = "d02b482d3e5431d9cdd63099566f3a8dcf8bc1064bfa580575773c5528ebfc59"

router = APIRouter()
blacklist = set()


crypt = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)


def authenticate_user(db: Session, dni: str, password: str):
    user: UserModel = get_user_by_dni(db, dni)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_user_access_token(user: UserModel):
    return create_access_token(str(user.id))


def get_user_by_dni(db: Session, dni: str):
    return db.query(UserModel).filter(UserModel.dni == dni).first()


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    try:

        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None


def invalidate_token(token: str):
    blacklist.add(token)


def is_token_revoked(token: str) -> bool:
    return token in blacklist


async def verify_token(authorization: str = Header(..., scheme="Bearer", include_in_schema=False)):
    try:
        token = authorization.split(" ")[1]
        if is_token_revoked(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="sdad token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalasid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalasid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return username
