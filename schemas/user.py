

from typing import Optional

from pydantic import BaseModel, Field

from models.user_model import Role
from schemas.category import Category


class UserBase(BaseModel):
    email: str
    is_active: bool
    first_name: str
    last_name: str
    dni: str = Field(..., max_length=8)
    avatar: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    role: str = Field(default=Role.player)


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    category: Optional[Category] = None

    class Config:
        orm_mode = True
