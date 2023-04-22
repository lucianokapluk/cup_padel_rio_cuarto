

from functools import wraps
from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from cruds import category_crud, user_crud
from cruds.authentication_crud import (authenticate_user,
                                       get_user_access_token, verify_token,
                                       verify_token_only_admin)
from db.database import Base, SessionLocal, engine, get_db
from schemas.user import User, UserCreate

security_scheme = HTTPBearer()
router = APIRouter(
    prefix="/users", tags=["users"])
(""" , dependencies=[Depends(security_scheme), Depends(verify_token)] """)


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_dni(db, dni=user.dni)
    if db_user:
        raise HTTPException(status_code=400, detail="DNI already registered")
    return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=List[User], )
def read_users(skip: int = 0, limit: int = 100,  db: Session = Depends(get_db),
               ):

    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User, dependencies=[Depends(verify_token_only_admin)])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/categories", response_model=User)
def assign_category_to_user(user_id: int, category_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_user.category_id = category_id
    db.commit()
    db.refresh(db_user)
    return db_user
