from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.database import Base
from models.tournament_inscription_model import TournamentInscriptionModel


class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    group_number = Column(Integer)
    tournament = relationship("TournamentModel", back_populates="groups")
    inscriptions = relationship(
        "TournamentInscriptionModel", back_populates="group")
