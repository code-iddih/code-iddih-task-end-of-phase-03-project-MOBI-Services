"""Add method, sender, and receiver columns to transactions table

Revision ID: afb76d1ae3da
Revises: b901834575f1
Create Date: 2024-09-18 18:10:07.321811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afb76d1ae3da'
down_revision: Union[str, None] = 'b901834575f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Creates a new temporary table with the desired schema
    op.create_table(
        'transactions_temp',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), default=sa.func.now(), nullable=True),
        sa.Column('method', sa.String(), nullable=True),
        sa.Column('sender', sa.String(), nullable=True),
        sa.Column('receiver', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copying data from the old table to the new table
    op.execute("""
        INSERT INTO transactions_temp (id, user_id, type, amount, timestamp, method, sender, receiver)
        SELECT id, user_id, type, amount, timestamp, NULL, NULL, NULL
        FROM transactions
    """)
    
    # Dropping the old table
    op.drop_table('transactions')
    
    # Renaming the new table to the original table name
    op.rename_table('transactions_temp', 'transactions')


def downgrade() -> None:
    # Creates the original table schema without the new columns
    op.create_table(
        'transactions_temp',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copies data back from the temporary table to the original table
    op.execute("""
        INSERT INTO transactions_temp (id, user_id, type, amount, timestamp)
        SELECT id, user_id, type, amount, timestamp
        FROM transactions
    """)
    
    # Drops the new table
    op.drop_table('transactions')
    
    # Renames the old table to the original table name
    op.rename_table('transactions_temp', 'transactions')
