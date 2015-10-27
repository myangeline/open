import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'sunshine'


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50))
    password = Column(String(50))
    admin = Column(Integer, default=0)
    name = Column(String(50))
    image = Column(String(500))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    user_id = Column(Integer)


class Blogs(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    title = Column(String(50))
    summary = Column(String(200), nullable=True)
    content = Column(Text)
    category_id = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())