from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class TournamentInscriptionModel(Base):
    __tablename__ = 'tournament_inscription'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    first_player_id = Column(Integer, ForeignKey("users.id"))
    second_player_id = Column(Integer, ForeignKey("users.id"))
    rate_date_time = Column(String)
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    tournament = relationship(
        "TournamentModel", back_populates="inscriptions")

    first_player = relationship(
        "UserModel", foreign_keys=[first_player_id], backref="first_player_inscriptions"
    )

    second_player = relationship(
        "UserModel", foreign_keys=[second_player_id], backref="second_player_inscriptions"
    )
