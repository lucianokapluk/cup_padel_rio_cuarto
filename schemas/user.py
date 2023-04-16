

from typing import Optional

from pydantic import BaseModel, Field

from schemas.category import Category


class UserBase(BaseModel):
    email: str
    is_active: bool
    first_name: str
    last_name: str
    dni: str = Field(..., max_length=8)
    avatar: str | None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    category: Category | None

    class Config:
        orm_mode = True
