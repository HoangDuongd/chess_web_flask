from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session


DATABASE = 'sqlite:///user.db'
engine = create_engine(DATABASE, echo=True)

Base = declarative_base()


# Tạo session và dùng scoped_session để quản lý thread-safe cho Flask
SessionLocal = scoped_session(sessionmaker(bind=engine))