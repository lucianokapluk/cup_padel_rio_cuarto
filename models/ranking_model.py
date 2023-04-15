from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.database import Base


class RankingModel(Base):
    __tablename__ = 'ranking'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    points = Column(Integer)
