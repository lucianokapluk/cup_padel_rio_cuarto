from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, orm

from db.database import Base


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

    category = orm.relationship("CategoryModel", back_populates="users")
