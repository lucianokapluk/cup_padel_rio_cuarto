from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.database import Base


class MatchModel(Base):
    __tablename__ = 'matches'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    first_inscription_id = Column(
        Integer, ForeignKey("tournament_inscription.id"))
    second_inscription_id = Column(
        Integer, ForeignKey("tournament_inscription.id"))
    winer = Column(Integer, ForeignKey("tournament_inscription.id"))
    tournament_id = Column(Integer, ForeignKey("tournament.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    result = Column(String)
    date_time_match = Column(String)
