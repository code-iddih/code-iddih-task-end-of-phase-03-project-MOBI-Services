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

# Generating a PDF report of a user's transactions
def generate_pdf_report(user_id):
    transactions = session.query(Transaction).filter_by(user_id=user_id).all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Transaction Report", ln=True, align='C')

    pdf.ln(10) 
    for txn in transactions:
        pdf.cell(200, 10, txt=f"{txn.timestamp}: {txn.type} - {txn.amount}", ln=True)

    pdf_file_name = f"transaction_report_{user_id}.pdf"
    pdf.output(pdf_file_name)
    print(f"PDF report generated Successfully... : {pdf_file_name}") 