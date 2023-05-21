
import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from cruds.authentication_crud import (authenticate_user,
                                       get_user_access_token, invalidate_token)
from db.database import get_db

router = APIRouter(
    prefix="/auth", tags=["Authentication"], )

security_scheme = HTTPBearer()


class LoginRequest(BaseModel):
    dni: str
    password: str


@router.post("/login/")
def login_for_access_token(login_body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_body.dni, login_body.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid dni or password")
    access_token = get_user_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout/")
async def logout(authorization: str):

    try:

        # Call a function to invalidate the token (e.g. add it to a blacklist)
        print(authorization)
        invalidate_token(authorization)
        return {"message": "Logout successful"}
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid toksen",
            headers={"WWW-Authenticate": "Bearer"},
        )

""" 
@router.post("/logout/")
async def logout(authorization: str = Header(..., scheme="Bearer")):
    try:

        # Call a function to invalidate the token (e.g. add it to a blacklist)
        print(authorization)
        invalidate_token(authorization)
        return {"message": "Logout successful"}
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid toksen",
            headers={"WWW-Authenticate": "Bearer"},
        )
 """
