#!/usr/bin/env python3

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

# Function to verify user login
def login():
    phone_number = input("Enter your phone number: ")
    user = session.query(User).filter_by(phone_number=phone_number).first()
    if user:
        balance = session.query(Balance).filter_by(user_id=user.id).first()
        if balance:
            print(f"Welcome {user.username}!")
            print(f"Your current balances are:")
            print(f"Airtime Balance: {balance.airtime_balance}")
            print(f"Bundles Balance: {balance.bundles_balance}")
            print(f"MPesa Balance: {balance.mpesa_balance}")
            log_activity(user.id, "Login")
            return user, balance
        else:
            print("No balance found for this user.")
            return None, None
    else:
        print("Phone number not found.")
        return None, None
    
    
# Function to Generate Random Numbers for new Users
def generate_phone_number():
    return '07' + ''.join([str(random.randint(0, 9)) for _ in range(8)])

# Function to regisster new user
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
    print(f"Welcome {new_user.username}! You have successfully earned a new line {phone_number}")
    print("You have been awarded free 50MB and 50 credit!")
    print("Your new balances are:")
    print(f"Airtime Balance: {new_balance.airtime_balance}")
    print(f"Bundles Balance: {new_balance.bundles_balance}")
    print(f"MPesa Balance: {new_balance.mpesa_balance}")
    
    # Logging the registration activity
    log_activity(new_user.id, "Register")
    
    return new_user, new_balance


# Function to Reord Transactions
def record_transaction(user_id, transaction_type, amount):
    new_transaction = Transaction(user_id=user_id, type=transaction_type, amount=amount)
    session.add(new_transaction)
    session.commit()

# Fuunction for Main Menu of Interaction
def main_menu(user, balance):
    while True:
        print("\n1. Buy airtime")
        print("2. Transfer airtime")
        print("3. Buy Bundles")
        print("4. Transfer Bundles")
        print("5. Send Money")
        print("6. Generate PDF Report")
        print("7. Logout")
        print("8. Back Home")
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
                print("Insufficient MPesa balance.")

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
                print("Insufficient airtime balance.")

        elif choice == '3':
            # Buy bundles functionality
            amount = float(input("Enter amount to buy bundles: "))
            payment_method = input("Choose payment method:\n1. MPesa\n2. Credit\nEnter 1 for MPesa or 2 for Credit: ")
            if payment_method == '1':
                if balance.mpesa_balance >= amount:
                    # Extracting  numeric part from bundles_balance
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
                    # Extractinng numeric part from bundles_balance
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
                print("Insufficient MPesa balance.")

        elif choice == '6':
            # Generate a PDF report of transactions
            generate_pdf_report(user.id)

        elif choice == '7':
            # Logout functionality
            print("Logging out...")
            break

        elif choice == '8':
            

        else:
            print("Invalid option. Please try again.")

# Function to handle registration , login
def main():
    welcome_message()
    choice = input("Enter 1 to Login or 2 to Register: ")
    if choice == '1':
        user, balance = login()
        if balance:
            main_menu(user, balance)
    elif choice == '2':
        user, balance = register()
        if balance:
            main_menu(user, balance)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
