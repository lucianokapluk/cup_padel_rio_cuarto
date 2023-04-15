from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.database import Base


class TournamentModel(Base):
    __tablename__ = 'tournament'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    inscription_id = Column(Integer, ForeignKey("tournament_inscription.id"))
    rate_date_time = Column(String)
