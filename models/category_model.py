from sqlalchemy import Boolean, Column, Integer, String

from db.database import Base


class CategoryModel(Base):
    __tablename__ = 'category'

    id = Column("id", Integer, primary_key=True,
                index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
