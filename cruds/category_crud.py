from sqlalchemy.orm import Session

from models.category_model import CategoryModel
from schemas.category import CategoryCreate, CategoryUpdate


# Get a category by ID
def get_category(db: Session, category_id: int):
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

# Get all categories


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CategoryModel).offset(skip).limit(limit).all()

# Create a new category


def create_category(db: Session, category: CategoryCreate):
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Update a category


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id).first()
    if not db_category:
        return None
    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

# Delete a category


def delete_category(db: Session, category_id: int):
    db_category = db.query(CategoryModel).filter(
        CategoryModel.id == category_id).first()
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category
