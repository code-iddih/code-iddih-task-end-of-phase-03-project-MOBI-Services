from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Balance, Transaction, ActivityLog, Base
from datetime import datetime
import random

# Database connection
DATABASE_URL = "sqlite:///mobi_services.db"
engine = create_engine(DATABASE_URL)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Balance, Transaction, ActivityLog, Base
from datetime import datetime
import random

# Database connection
DATABASE_URL = "sqlite:///mobi_services.db"
engine = create_engine(DATABASE_URL)

# Create all tables (in case they don't exist yet)
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Function to generate a random phone number starting with 07 and a total of 10 digits
def generate_phone_number():
    return '07' + str(random.randint(10000000, 99999999))


# Populating the tables with sample data
def seed_data():
    # Sample users
    users = [
        User(phone_number=generate_phone_number(), username='Eric'),
        User(phone_number=generate_phone_number(), username='James'),
        User(phone_number=generate_phone_number(), username='Kim'),
    ]
    session.add_all(users)
    session.commit()

    # Sample balances
    balances = [
        Balance(user_id=users[0].id, airtime_balance=50.0, bundles_balance=200.0, mpesa_balance=1000.0),
        Balance(user_id=users[1].id, airtime_balance=30.0, bundles_balance=100.0, mpesa_balance=500.0),
        Balance(user_id=users[2].id, airtime_balance=20.0, bundles_balance=50.0, mpesa_balance=300.0),
    ]
    session.add_all(balances)
    session.commit()

    # Sample transactions
    transactions = [
        Transaction(user_id=users[0].id, type='Buy Airtime', amount=20.0, timestamp=datetime.now()),
        Transaction(user_id=users[1].id, type='Send Money', amount=50.0, timestamp=datetime.now()),
        Transaction(user_id=users[2].id, type='Buy Bundles', amount=10.0, timestamp=datetime.now()),
    ]
    session.add_all(transactions)
    session.commit()

    # Sample activity logs
    activity_logs = [
        ActivityLog(user_id=users[0].id, action="Login", timestamp=datetime.now()),
        ActivityLog(user_id=users[1].id, action="Register", timestamp=datetime.now()),
        ActivityLog(user_id=users[2].id, action="Buy Bundles", timestamp=datetime.now()),
    ]
    session.add_all(activity_logs)
    session.commit()

    print("Sample data inserted successfully!")

# Clearing existing data and seed new data
seed_data()

# Close session
session.close()


