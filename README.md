# End of Phase 3 Project : MOBISercices

## Overiew

Mobi Services is a command-line application designed to facilitate various mobile transactions, making it easy for users to manage their accounts and finances. Users can quickly get a new line, buy airtime, and transfer airtime to others. The application also allows users to purchase data bundles and transfer them between accounts, as well as send and receive money securely. For administrators, there is an option to run the application and access all user activity logs, ensuring effective monitoring and management of transactions.

## Features

- **User Registration & Login:** Create new user accounts and login securely.

- **Transaction Management:** Buy airtime, send money, and transfer bundles between users.

- **Activity Logging:** Track user activities and generate a detailed transaction report.

- **Admin Functions:** Special admin access for viewing activity logs and managing users.

- **PDF Reports:** Generate transaction reports in PDF format for easy sharing and review.

## Topics

- Python Fundamentals
- SQLAlchemy Migrations
- SQLAlchemy Relationships
- Class and Instance Methods
- SQLAlchemy Querying

## Technologies

- Python
- SQLAlchemy
- SQLite
- FPDF


We have four models: `User`, `Balance`, `Transaction`, and `ActivityLog`.

For our purposes, a `User` has one `Balance`, many `Transaction`, and many `ActivityLog`.

A `Balance` is associated with one `User`, tracking their airtime, bundles, and MPesa `Balance`.

A `Transaction` belongs to one `User` and records details of each tr`Transaction`ansaction.

An `ActivityLog` also belongs to one `User` and captures user activities for auditing.

The User to `Transaction` and `User` to `ActivityLog` relationships are one-to-many, while the `User` to `Balance` relationship is one-to-one.

The **schema** currently looks like this:

### `users` Table

| Column        | Type   |
| ------------- | ------ |
| phone_number  | String |
| username      | String |

### `balances` Table

| Column          | Type    |
| --------------- | ------  |
| user_id         | integer |
| airtime_balance | float   |
| bundles_balance | string  |
| mpesa_balance   | float   |

### `transactions` Table

| Column     | Type    |
| ---------- | ------  |
| user_id    | integer |
| type       | float   |
| amount     | string  |
| timestamp  | float   |
| method     | float   |
| sender     | float   |
| receiver   | float   |

### `activity_log` Table

| Column     | Type    |
| ---------- | ------  |
| user_id    | integer |
| action     | string  |
| timestamp  | float   |

## Function Descriptions

### Main Functions

- `main():`
  - Starts the application and displays the main menu for user interaction (login, register, exit).

- `login():`
  - Prompts the user for their phone number and verifies their credentials. If valid, it displays the user's home page.

- `register():`
  - Allows new users to create an account. Generates a phone number and initializes balances.

- `display_home(user, balance):`
  - Shows the user's current balance and a welcome message.

- `main_menu(user, balance):`
  - Displays the options available to the user after logging in, including transaction functionalities.

- `log_activity(user_id, action, details=""):`
  - Records user activities for tracking purposes.

### Transaction Functions

- `record_transaction(user_id, transaction_type, amount, method=None, sender=None, receiver=None):`
  - Records a transaction in the database.

- `generate_pdf_report(user_id):`
  - Creates a PDF report of the user's transaction history.

### Transaction Actions

1. **Buy Airtime:** Allows users to purchase airtime using their MPesa balance.

2. **Transfer Airtime:** Enables users to transfer airtime to another user.

3. **Buy Bundles:** Users can buy data bundles using either MPesa or airtime.

4. **Transfer Bundles:** Users can transfer their data bundles to others.

5. **Send Money:** Users can send money to other users using MPesa.

### Admin action

**View Activity Logs:** Admin users can view all user activity logs.
 

## Setup Instructions
1. Clone the repository.
```txt
git clone https://git@github.com:code-iddih/code-iddih-task-end-of-phase-03-project-MOBI-Services.git
```
1. Navigate to the project directory.

3. Get inside the environment
```txt
pipenv install
pipenv shell
```
4. Install dependencies
```txt
pipenv install sqlalchemy alembic fpdf
```
5. Run the migration to set up your database schema:

```txt
Run alembic upgrade head
```
6. Seed the database with sample data:
```txt
python3 seed.py
```
5. Enjoy!!!

## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.





