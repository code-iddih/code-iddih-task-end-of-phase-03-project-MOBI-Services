import random
from fpdf import FPDF
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Balance, Transaction, ActivityLog, Base

engine = create_engine('sqlite:///mobi_services.db')
Session = sessionmaker(bind=engine)
session = Session()

# Printing a wlecoming message
def welcome_message():
    print("\nWelcome to MOBILE SERVICES\n")

# Log user activities
def log_activity(user_id, action):
    new_activity = ActivityLog(user_id=user_id, action=action)
    session.add(new_activity)
    session.commit()