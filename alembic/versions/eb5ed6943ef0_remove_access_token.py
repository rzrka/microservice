"""remove access token

Revision ID: eb5ed6943ef0
Revises: 9286fdc62b3f
Create Date: 2024-10-18 02:49:18.318573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eb5ed6943ef0'
down_revision: Union[str, None] = '9286fdc62b3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('access_tokens', schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_tokens',
    sa.Column('access_token', sa.VARCHAR(length=1024), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('expiration_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['public.users.id'], name='access_tokens_user_id_fkey'),
    sa.PrimaryKeyConstraint('access_token', name='access_tokens_pkey'),
    schema='public'
    )
    # ### end Alembic commands ###