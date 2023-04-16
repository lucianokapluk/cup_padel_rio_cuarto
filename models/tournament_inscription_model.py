from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class TournamentInscriptionModel(Base):
    __tablename__ = 'tournament_inscription'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    first_player = Column(Integer, ForeignKey("users.id"))
    second_player = Column(Integer, ForeignKey("users.id"))
    rate_date_time = Column(String)
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    tournament = relationship(
        "TournamentModel", back_populates="inscriptions")
