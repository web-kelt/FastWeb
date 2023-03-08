from sqlalchemy import Column, String, Integer, Boolean

from src.database.base import Base, choose_db, check_db


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    access_token = Column(String)
    is_admin = Column(Boolean)

    def __init__(self, login, access_token, is_admin, id=5000):
        self.login = login
        self.access_token = access_token
        self.is_admin = is_admin



class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    genge = Column(String)


Base.metadata.create_all(bind=choose_db(arg_db=check_db))
