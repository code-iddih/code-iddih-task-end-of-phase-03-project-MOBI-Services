from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

DATABASE_URL = "sqlite:///mobi_services.db" 

engine = create_engine('sqlite:///mobi_services.db')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(10), unique=True, nullable=False)
    username = Column(String, nullable=False)
    balance = relationship("Balance", back_populates="user")
    activities = relationship("ActivityLog", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class Balance(Base):
    __tablename__ = 'balances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    airtime_balance = Column(Float, default=0.0)
    bundles_balance = Column(String, default="0MB")  # New bundles balance column
    mpesa_balance = Column(Float, default=0.0)
    user = relationship("User", back_populates="balance")


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="transactions")

class ActivityLog(Base):
    __tablename__ = 'activity_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="activities")



