from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base
from models.tournament_model import TournamentModel
from models.user_model import UserModel


class CategoryModel(Base):
    __tablename__ = 'category'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    users = relationship(UserModel, back_populates="category")
    category_torunament = relationship(
        TournamentModel, back_populates="category")
