#!/usr/bin/env python3

import random
from fpdf import FPDF
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Balance, Transaction, ActivityLog, Base
from colors import *

engine = create_engine('sqlite:///mobi_services.db')
Session = sessionmaker(bind=engine)
session = Session()

# Printing a welcoming message
def welcome_message():
    print(f"\n{YELLOW}Welcome to MOBILE SERVICES{RESET}\n")

# Log user activities
def log_activity(user_id, action):
    new_activity = ActivityLog(user_id=user_id, action=action)
    session.add(new_activity)
    session.commit()

# Function to verify user login
def login():
    phone_number = input("Enter your phone number: ")
    user = session.query(User).filter_by(phone_number=phone_number).first()
    if user:
        balance = session.query(Balance).filter_by(user_id=user.id).first()
        if balance:
            display_home(user, balance)  # Display balances upon login
            log_activity(user.id, "Login")
            return user, balance
        else:
            print("No balance found for this user.")
            return None, None
    else:
        print("Phone number not found.")
        return None, None

# Function to generate random numbers for new users
def generate_phone_number():
    return '07' + ''.join([str(random.randint(0, 9)) for _ in range(8)])

# Function to display user balances
def display_home(user, balance):
    print(f"\nWelcome {user.username}!")
    print("\nYour current balances are:")
    print(f"Airtime Balance: {balance.airtime_balance}")
    print(f"Bundles Balance: {balance.bundles_balance}")
    print(f"MPesa Balance: {balance.mpesa_balance}\n")
    print("\n1. Buy airtime")
    print("2. Transfer airtime")
    print("3. Buy Bundles")
    print("4. Transfer Bundles")
    print("5. Send Money")
    print("6. Generate PDF Report")
    print("7. Logout")
    print("8. Back Home")

# Function to register a new user
def register():
    name = input("Enter your name: ")
    phone_number = generate_phone_number()
    
    # Creating a new user
    new_user = User(phone_number=phone_number, username=name)
    session.add(new_user)
    session.commit()
    
    # Awarding 50MB and 50 credit upon registration
    new_balance = Balance(user_id=new_user.id, airtime_balance=50, bundles_balance="50MB", mpesa_balance=0)
    session.add(new_balance)
    session.commit()

    # Displaying success message and balances vertically
    print(f"\nYou have successfully earned a new line {phone_number}")
    print("You have also been awarded free 50MB and 50 credit!")
    
    # Logging the registration activity
    log_activity(new_user.id, "Register")

    display_home(new_user, new_balance)
    main_menu(new_user, new_balance)
    
    return new_user, new_balance

# Function to record transactions
def record_transaction(user_id, transaction_type, amount, method=None, sender=None, receiver=None):
    new_transaction = Transaction(
        user_id=user_id,
        type=transaction_type,
        amount=amount,
        method=method,
        sender=sender,
        receiver=receiver
    )
    session.add(new_transaction)
    session.commit()

# Generating a PDF report of a user's transactions
def generate_pdf_report(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    transactions = session.query(Transaction).filter_by(user_id=user_id).all()

    if not user:
        print("User not found.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adding User Name
    pdf.cell(200, 10, txt=f"Name of the user: {user.username}", ln=True, align='L')

    # Adding Table Header
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(30, 10, "Date", 1)
    pdf.cell(40, 10, "Type", 1)
    pdf.cell(50, 10, "Method", 1)
    pdf.cell(30, 10, "Sender", 1)
    pdf.cell(30, 10, "Receiver", 1)
    pdf.cell(40, 10, "Amount", 1, ln=True)

    # Adding Transaction Data
    pdf.set_font("Arial", size=9)
    for txn in transactions:
        txn_date = txn.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        txn_type = txn.type
        txn_method = txn.method if txn.method else 'N/A'
        txn_sender = txn.sender if txn.sender else 'N/A'
        txn_receiver = txn.receiver if txn.receiver else 'N/A'
        txn_amount = f"{txn.amount:.2f}"

        pdf.cell(30, 10, txn_date, 1)
        pdf.cell(40, 10, txn_type, 1)
        pdf.cell(50, 10, txn_method, 1)
        pdf.cell(30, 10, txn_sender, 1)
        pdf.cell(30, 10, txn_receiver, 1)
        pdf.cell(40, 10, txn_amount, 1, ln=True)

    pdf_file_name = f"transaction_report_{user_id}.pdf"
    pdf.output(pdf_file_name)
    print(f"PDF report generated successfully: {pdf_file_name}")


# Function for main menu interaction
def main_menu(user, balance):
    while True:
        choice = input("Choose an option: ")

        if choice == '1':
            # Buy airtime functionality
            amount = float(input("Enter amount to buy airtime: "))
            if balance.mpesa_balance >= amount:
                balance.airtime_balance += amount
                balance.mpesa_balance -= amount
                session.commit()
                record_transaction(user.id, 'Buy Airtime', amount)
                print(f"Airtime purchased. New balance: {balance.airtime_balance}")
            else:
                print(f"Insufficient MPesa balance. Your current balance is {balance.mpesa_balance}")

        elif choice == '2':
            # Transfer airtime functionality
            amount = float(input("Enter amount to transfer airtime: "))
            if balance.airtime_balance >= amount:
                recipient_phone = input("Enter recipient phone number: ")
                recipient = session.query(User).filter_by(phone_number=recipient_phone).first()
                if recipient:
                    recipient_balance = session.query(Balance).filter_by(user_id=recipient.id).first()
                    balance.airtime_balance -= amount
                    recipient_balance.airtime_balance += amount
                    session.commit()
                    record_transaction(user.id, 'Transfer Airtime', amount)
                    print(f"Airtime transferred to {recipient_phone}. New balance: {balance.airtime_balance}")
                else:
                    print("Recipient not found.")
            else:
                print(f"Insufficient airtime balance. Your current balance is {balance.airtime_balance}")

        elif choice == '3':
            # Buy bundles functionality
            amount = float(input("Enter amount to buy bundles: "))
            payment_method = input("Choose payment method:\n1. MPesa\n2. Credit\nEnter 1 for MPesa or 2 for Credit: ")
            if payment_method == '1':
                if balance.mpesa_balance >= amount:
                    current_bundles = float(balance.bundles_balance.replace("MB", ""))
                    balance.bundles_balance = f"{int(current_bundles + amount)}MB"
                    balance.mpesa_balance -= amount
                    session.commit()
                    record_transaction(user.id, 'Buy Bundles', amount)
                    print(f"Bundles purchased with MPesa. New balance: {balance.bundles_balance}")
                else:
                    print(f"Insufficient MPesa balance. Your current balance is {balance.mpesa_balance}")
            elif payment_method == '2':
                if balance.airtime_balance >= amount:
                    current_bundles = float(balance.bundles_balance.replace("MB", ""))
                    balance.bundles_balance = f"{int(current_bundles + amount)}MB"
                    balance.airtime_balance -= amount
                    session.commit()
                    record_transaction(user.id, 'Buy Bundles', amount)
                    print(f"Bundles purchased with Credit. New balance: {balance.bundles_balance}")
                else:
                    print(f"Insufficient airtime balance. Your current balance is {balance.airtime_balance}")
            else:
                print("Invalid payment method selected.")

        elif choice == '4':
            # Transfer bundles functionality
            amount = float(input("Enter amount to transfer bundles: "))
            if int(balance.bundles_balance[:-2]) >= amount:
                recipient_phone = input("Enter recipient phone number: ")
                recipient = session.query(User).filter_by(phone_number=recipient_phone).first()
                if recipient:
                    recipient_balance = session.query(Balance).filter_by(user_id=recipient.id).first()
                    balance.bundles_balance = f"{int(balance.bundles_balance[:-2]) - int(amount)}MB"
                    recipient_balance.bundles_balance = f"{int(recipient_balance.bundles_balance[:-2]) + int(amount)}MB"
                    session.commit()
                    record_transaction(user.id, 'Transfer Bundles', amount)
                    print(f"Bundles transferred to {recipient_phone}. New balance: {balance.bundles_balance}")
                else:
                    print("Recipient not found.")
            else:
                print("Insufficient bundles balance.")

        elif choice == '5':
            # Send money functionality
            amount = float(input("Enter amount to send: "))
            if balance.mpesa_balance >= amount:
                recipient_phone = input("Enter recipient phone number: ")
                recipient = session.query(User).filter_by(phone_number=recipient_phone).first()
                if recipient:
                    balance.mpesa_balance -= amount
                    recipient_balance = session.query(Balance).filter_by(user_id=recipient.id).first()
                    recipient_balance.mpesa_balance += amount
                    session.commit()
                    record_transaction(user.id, 'Send Money', amount)
                    print(f"Money sent to {recipient_phone}. New MPesa balance: {balance.mpesa_balance}")
                else:
                    print("Recipient not found.")
            else:
                print(f"Insufficient MPesa balance. Your current balance is {balance.mpesa_balance}")

        elif choice == '6':
            # Generate a PDF report of transactions
            generate_pdf_report(user.id)

        elif choice == '7':
            # Logout functionality
            print("Logging out...")
            break

        elif choice == '8':
            display_home(user, balance)  # Show the home screen view
            continue  # Continue the loop to allow further options

        else:
            print("Invalid option. Please try again.")

# Function to handle registration and login
def main():
    welcome_message()
    choice = input("1. Register\n2. Login\nChoose an option: ")

    if choice == '1':
        user, balance = register()
        if user and balance:
            main_menu(user, balance)
    elif choice == '2':
        user, balance = login()
        if user and balance:
            main_menu(user, balance)
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
