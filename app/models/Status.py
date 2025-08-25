from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import Base

class Status(Base):
    __tablename__ = 'Status'
    id = Column(Integer, unique=True, primary_key=True)
    blitz_chess = Column(Integer, default = 500, nullable=False)
    lightning = Column(Integer, default = 500, nullable=False)
    super_lightning = Column(Integer, default = 500, nullable=False)
