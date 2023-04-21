
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from cruds import category_crud
from db.database import SessionLocal, engine, get_db
from schemas.category import Category, CategoryCreate, CategoryUpdate

security_scheme = HTTPBearer()

router = APIRouter(
    prefix="/category", tags=["categories"])


# Users Endpoints


@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Get all categories


@router.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = category_crud.get_categories(db, skip=skip, limit=limit)
    return categories

# Create a new category


@router.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = category_crud.create_category(db, category=category)
    return db_category

# Update a category


@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = category_crud.update_category(
        db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Delete a category


@router.delete("/categories/{category_id}", response_model=Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
