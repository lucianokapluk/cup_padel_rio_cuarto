from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base
from models.tournament_inscription_model import TournamentInscriptionModel


class TournamentModel(Base):
    __tablename__ = 'tournament'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    mode = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    start_date_time = Column(String)
    end_date_time = Column(String)

 # Definición de la relación con la tabla CategoryModel
    category = relationship(
        "CategoryModel", back_populates="category_torunament")
    # Definición de la relación con la tabla TournamentInscription

    inscriptions = relationship(
        "TournamentInscriptionModel", back_populates="tournament", foreign_keys=[TournamentInscriptionModel.tournament_id])

    groups = relationship("GroupModel", back_populates="tournament")
