from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user_model import UserModel
from schemas import user


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_dni(db: Session, dni: str):
    return db.query(UserModel).filter(UserModel.dni == dni).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate):

    user.password = hash_password(user.password)
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


crypt = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return crypt.hash(password)
