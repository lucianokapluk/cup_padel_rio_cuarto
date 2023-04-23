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


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def patch_user(db: Session, user_id: int, user_data: user.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


crypt = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return crypt.hash(password)
