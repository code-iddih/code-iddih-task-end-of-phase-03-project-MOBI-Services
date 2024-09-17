from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

DATABASE_URL = "sqlite:///mobi_services.db" 

engine = create_engine(DATABASE_URL)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    balance = relationship("Balance", back_populates="user")
    activities = relationship("ActivityLog", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

Base.metadata.create_all(engine)