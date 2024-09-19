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

# Menu Option for Admin Users
admin_menu_options = (
    ('1', "Buy Airtime"),
    ('2', "Transfer Airtime"),
    ('3', "Buy Bundles"),
    ('4', "Transfer Bundles"),
    ('5', "Send Money"),
    ('6', "Generate Transactions PDF"),
    ('7', "Logout"),
    ('8', "Back Home"),
    ('9', "View Activity Logs")  # For Admins only
)

# Menu Option for Regular Users
user_menu_options = (
    ('1', "Buy Airtime"),
    ('2', "Transfer Airtime"),
    ('3', "Buy Bundles"),
    ('4', "Transfer Bundles"),
    ('5', "Send Money"),
    ('6', "Generate Transactions PDF"),
    ('7', "Logout"),
    ('8', "Back Home"),
)

# Main Menu Option
main_menu_options = (
    ('1', "Login"),
    ('2', "Register"),
    ('3', "Exit")
)

# Printing a welcoming message
def welcome_message():
    print(f"\n{YELLOW}{BOLD}Welcome to MOBILE SERVICES!{RESET}{RESET}\n")

# Log user activities
def log_activity(user_id, action, details=""):
    new_activity = ActivityLog(user_id=user_id, action=f"{action} {details}")
    session.add(new_activity)
    session.commit()

# Function to verify user login
def login():
    phone_number = input("Enter your phone number: ")
    user = session.query(User).filter_by(phone_number=phone_number).first()
    if user:
        balance = session.query(Balance).filter_by(user_id=user.id).first()
        if balance:
            display_home(user, balance)
            log_activity(user.id, "logged in")
            return user, balance
    print(f"{RED}Phone number not found or no balance found.{RESET}")
    return None, None

# Function to generate random numbers for new users
def generate_phone_number():
    return '07' + ''.join([str(random.randint(0, 9)) for _ in range(8)])

# Function to display user balances
def display_home(user, balance):
    print(f"\nWelcome {GREEN}{BOLD}{user.username}{RESET}{RESET}!")
    print("\nYour current balances are:")
    print("-------------------------")
    print(f"Airtime Balance: {BLUE}{balance.airtime_balance}{RESET}")
    print(f"Bundles Balance: {BLUE}{balance.bundles_balance}{RESET}")
    print(f"MPesa Balance: {BLUE}{balance.mpesa_balance}{RESET}")
    print("-------------------------")

# Validate user Name
def is_valid_username(username):
    return bool(username) and username.isalpha()

# Function to register a new user
def register():
    while True:
        name = input("Enter your name: ")
        if is_valid_username(name):
            break
        else:
            print(f"{RED}Invalid name. Please enter a valid name.{RESET}")
    
    phone_number = generate_phone_number()
    
    new_user = User(phone_number=phone_number, username=name)
    session.add(new_user)
    session.commit()
    
    new_balance = Balance(user_id=new_user.id, airtime_balance=50, bundles_balance="50MB", mpesa_balance=0)
    session.add(new_balance)
    session.commit()

    print(f"\nYou have successfully earned a new line {GREEN}{phone_number}{RESET}")
    print(f"You have also been awarded free {GREEN}50MB and 50 credit!{RESET}")
    
    log_activity(new_user.id, "registered")
    
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
        print(f"{RED}User not found.{RESET}")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Name of the user: {user.username}", ln=True, align='L')

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(30, 10, "Date", 1)
    pdf.cell(40, 10, "Type", 1)
    pdf.cell(50, 10, "Method", 1)
    pdf.cell(30, 10, "Sender", 1)
    pdf.cell(30, 10, "Receiver", 1)
    pdf.cell(40, 10, "Amount", 1, ln=True)

    pdf.set_font("Arial", size=9)
    for txn in transactions:
        txn_date = txn.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        txn_type = txn.type
        txn_amount = f"{txn.amount:.2f}"

        txn_method = txn.method if txn.method else 'N/A'
        txn_sender = txn.sender if txn.sender else user.username
        txn_receiver = txn.receiver if txn.receiver else 'N/A'

        pdf.cell(30, 10, txn_date, 1)
        pdf.cell(40, 10, txn_type, 1)
        pdf.cell(50, 10, txn_method, 1)
        pdf.cell(30, 10, txn_sender, 1)
        pdf.cell(30, 10, txn_receiver, 1)
        pdf.cell(40, 10, txn_amount, 1, ln=True)

    pdf_file_name = f"transaction_report_{user_id}.pdf"
    pdf.output(pdf_file_name)
    print(f"PDF report generated successfully: {pdf_file_name}")

# Function to View Logs
def view_activity_logs():
    activities = session.query(ActivityLog).all()
    print(f"\n{BG_CYAN}Activity Log for All Users:{RESET}")
    
    for activity in activities:
        user = session.query(User).filter_by(id=activity.user_id).first()
        if user:
            timestamp_str = activity.timestamp.strftime('%I:%M %p on %Y-%m-%d')
            print(f"User {user.username} {activity.action} at {timestamp_str}")

# Function for main menu interaction
def main_menu(user, balance):
    while True:
        # Determine which menu options to display
        if user.phone_number == "0756668183":  # Check if the user is admin
            menu = admin_menu_options
        else:
            menu = user_menu_options

        # Display menu options
        print("\nChoose Option :")
        # Iterating the List
        for option in menu:
            print(f"{option[0]}. {BOLD}{option[1]}{RESET}")
        
        choice = input("\nChoose Option: ")
        
        # Buy Airtime
        if choice == '1':
            amount = float(input("Enter amount to buy airtime: "))
            if balance.mpesa_balance >= amount:
                balance.airtime_balance += amount
                balance.mpesa_balance -= amount
                session.commit()
                record_transaction(user.id, 'Buy Airtime', amount, method='mpesa', sender=user.username)
                log_activity(user.id, f"purchased airtime worth {amount} using MPesa")
                print(f"Airtime purchased. New balance: {BLUE}{balance.airtime_balance}{RESET}")
            else:
                print(f"{RED}Insufficient MPesa balance. Your current balance is {BLUE}{balance.mpesa_balance}{RESET}")

        # Transfer Airtime
        elif choice == '2':
            amount = float(input("Enter amount to transfer airtime: "))
            if balance.airtime_balance >= amount:
                recipient_phone = input("Enter recipient phone number: ")
                recipient = session.query(User).filter_by(phone_number=recipient_phone).first()
                if recipient:
                    recipient_username = recipient.username
                    recipient_balance = session.query(Balance).filter_by(user_id=recipient.id).first()
                    balance.airtime_balance -= amount
                    recipient_balance.airtime_balance += amount
                    session.commit()
                    record_transaction(user.id, 'Transfer Airtime', amount, method='airtime', sender=user.username, receiver=recipient_username)
                    log_activity(user.id, f"transferred airtime worth {amount} to {recipient_phone}")
                    print(f"Airtime transferred to {recipient_phone}. Your new airtime balance: {BLUE}{balance.airtime_balance}{RESET}")
                else:
                    print(f"{RED}Recipient not found.{RESET}")
            else:
                print(f"Insufficient airtime balance. Your current balance is {BLUE}{balance.airtime_balance}{RESET}")

        # Buy Bundles
        elif choice == '3':
            amount = int(input("Enter amount of bundles to buy: "))
            payment_method = input("Choose payment method:\n1. MPesa\n2. Credit\nEnter 1 for MPesa or 2 for Credit: ")
            # Buying Bundles Using Mpesa
            if payment_method == '1':
                if balance.mpesa_balance >= amount:
                    current_bundles = balance.bundles_balance
                    new_bundles = f"{int(current_bundles.split('MB')[0]) + int(amount)}MB"
                    balance.bundles_balance = new_bundles
                    balance.mpesa_balance -= amount
                    session.commit()
                    record_transaction(user.id, 'Buy Bundles', amount, method='MPesa')
                    log_activity(user.id, f"bought {amount}MB of bundles using MPesa")
                    print(f"Bundles purchased. New bundles balance: {BLUE}{balance.bundles_balance}{RESET}")
                else:
                    print(f"{RED}Insufficient MPesa balance. Your current balance is {BLUE}{balance.mpesa_balance}{RESET}")

            # Buying Bundles Using Airtime
            elif payment_method == '2':
                if balance.airtime_balance >= amount:
                    current_bundles = balance.bundles_balance
                    new_bundles = f"{int(current_bundles.split('MB')[0]) + int(amount)}MB"
                    balance.bundles_balance = new_bundles
                    balance.airtime_balance -= amount
                    session.commit()
                    record_transaction(user.id, 'Buy Bundles', amount, method='Credit')
                    log_activity(user.id, f"bought {amount}MB of bundles using Credit")
                    print(f"Bundles purchased. New bundles balance: {BLUE}{balance.bundles_balance}{RESET}")
                else:
                    print(f"{RED}Insufficient airtime balance. Your current balance is {BLUE}{balance.airtime_balance}{RESET}")
        
        # Transfer Bundles
        elif choice == '4':
            amount = int(input("Enter amount of bundles to transfer: "))
            if int(balance.bundles_balance.split('MB')[0]) >= amount:
                recipient_phone = input("Enter recipient phone number: ")
                recipient = session.query(User).filter_by(phone_number=recipient_phone).first()
                if recipient:
                    recipient_balance = session.query(Balance).filter_by(user_id=recipient.id).first()
                    current_bundles = int(balance.bundles_balance.split('MB')[0])
                    new_bundles = f"{current_bundles - amount}MB"
                    balance.bundles_balance = new_bundles
                    recipient_balance.bundles_balance = f"{int(recipient_balance.bundles_balance.split('MB')[0]) + amount}MB"
                    session.commit()
                    record_transaction(user.id, 'Transfer Bundles', amount, method='bundles', sender=user.username, receiver=recipient.username)
                    log_activity(user.id, f"transferred {amount}MB of bundles to {recipient_phone}")
                    print(f"Bundles transferred to {recipient_phone}. Your new bundles balance: {BLUE}{balance.bundles_balance}{RESET}")
                else:
                    print(f"{RED}Recipient not found.{RESET}")
            else:
                print(f"Insufficient bundles balance. Your current balance is {BLUE}{balance.bundles_balance}{RESET}")

        # Send Money
        elif choice == '5':
            amount = float(input("Enter amount to send: "))
            if balance.mpesa_balance >= amount:
                recipient_phone = input("Enter recipient phone number: ")
                recipient = session.query(User).filter_by(phone_number=recipient_phone).first()
                if recipient:
                    balance.mpesa_balance -= amount
                    session.commit()
                    record_transaction(user.id, 'Send Money', amount, method='MPesa', sender=user.username, receiver=recipient.username)
                    log_activity(user.id, f"sent {amount} to {recipient_phone}")
                    print(f"Money sent to {recipient_phone}. Your new MPesa balance: {BLUE}{balance.mpesa_balance}{RESET}")
                else:
                    print(f"{RED}Recipient not found.{RESET}")
            else:
                print(f"{RED}Insufficient MPesa balance. Your current balance is {BLUE}{balance.mpesa_balance}{RESET}")

        # Generate Transactions pdf
        elif choice == '6':
            generate_pdf_report(user.id)

        # Logout  
        elif choice == '7':
            log_activity(user.id, "logged out")
            print(f"{GREEN}You have been logged out successfully.{RESET}")
            return

        # Back Home
        elif choice == '8':
            display_home(user, balance)  # Go back to main menu

        # View Activity Logs
        elif choice == '9' and user.phone_number == "0756668183":
            view_activity_logs()

        else:
            print(f"{RED}Invalid option. Please try again.{RESET}")

# Function to handle registration , login & Exit
def main():
    welcome_message()
    
    while True:
        print("\nMain Menu:")
        for option in main_menu_options:
            print(f"{option[0]}. {BOLD}{option[1]}{RESET}")

        choice = input("\nChoose Option: ")
        
        if choice == '1':
            user, balance = login()
            if user:
                main_menu(user, balance)
        
        elif choice == '2':
            user, balance = register()
            if user:
                main_menu(user, balance)
        
        elif choice == '3':
            print(f"Thank you for using Mobile Services! {GREEN}Goodbye.{RESET}")
            break

        else:
            print(f"{RED}Invalid option. Please try again.{RESET}")

if __name__ == "__main__":
    main()
