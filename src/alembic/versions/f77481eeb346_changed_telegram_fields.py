"""Changed telegram fields

Revision ID: f77481eeb346
Revises: 59f93e7c4bc8
Create Date: 2024-09-20 07:37:53.502302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f77481eeb346'
down_revision: Union[str, None] = '59f93e7c4bc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_user', 'telegram_username',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=32),
               existing_nullable=True)
    op.alter_column('users_user', 'telegram_chat_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=128),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users_user', 'telegram_chat_id',
               existing_type=sa.String(length=128),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('users_user', 'telegram_username',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)
    # ### end Alembic commands ###
