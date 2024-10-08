"""renamed fields

Revision ID: 63d7c2f286b0
Revises: f77481eeb346
Create Date: 2024-09-20 11:02:31.019831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63d7c2f286b0'
down_revision: Union[str, None] = 'f77481eeb346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_user', 'first_name',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('users_user', 'last_name',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_user', 'last_name',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    op.alter_column('users_user', 'first_name',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###
