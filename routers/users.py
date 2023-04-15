

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from cruds import category_crud, user_crud
from db.database import Base, SessionLocal, engine
from schemas.user import User, UserCreate
from services.jwt_auth_users import authenticate_user, get_user_access_token

router = APIRouter(
    prefix="/users", tags=["users"], )

security_scheme = HTTPBearer()

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_dni(db, dni=user.dni)
    if db_user:
        raise HTTPException(status_code=400, detail="DNI already registered")
    return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(security_scheme)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/login/")
def login_for_access_token(dni: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, dni, password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid dni or password")
    access_token = get_user_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

# Assign a category to a user


@router.post("/users/{user_id}/categories", response_model=User)
def assign_category_to_user(user_id: int, category_id: int, db: Session = Depends(get_db), token: str = Depends(security_scheme)):
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
