"""Change Phone format and bundle balance format

Revision ID: b901834575f1
Revises: 39dcd47166dc
Create Date: 2024-09-17 23:41:29.898268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b901834575f1'
down_revision: Union[str, None] = '39dcd47166dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('balances', 'bundles_balance',
               existing_type=sa.FLOAT(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('balances', 'bundles_balance',
               existing_type=sa.String(),
               type_=sa.FLOAT(),
               existing_nullable=True)
    # ### end Alembic commands ###
