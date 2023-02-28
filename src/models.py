from sqlalchemy import Column, String, Integer, Boolean

from src.database.base import Base, choose_db, check_db


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)


Base.metadata.create_all(bind=choose_db(arg_db=check_db))
