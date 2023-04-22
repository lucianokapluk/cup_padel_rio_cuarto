from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base
from models.tournament_inscription_model import TournamentInscriptionModel


class Role(str, Enum):
    admin = "admin"
    staff = "staff"
    player = "player"


class UserModel(Base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    dni = Column(String(8),)
    email = Column(String,  unique=True, index=True)
    password = Column(String)
    avatar = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    role = Column(String, default=Role.player)
    category = relationship("CategoryModel", back_populates="users")
