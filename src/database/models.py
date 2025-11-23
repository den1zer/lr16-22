from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=func.now())

class CatFact(Base):
    __tablename__ = "cat_facts"
    
    id = Column(Integer, primary_key=True, index=True)
    fact = Column(String, nullable=False)
    length = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())