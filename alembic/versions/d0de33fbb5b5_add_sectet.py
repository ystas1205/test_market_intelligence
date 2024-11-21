"""Add Sectet

Revision ID: d0de33fbb5b5
Revises: 
Create Date: 2024-11-17 14:45:56.717628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0de33fbb5b5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('secrets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secret', sa.String(), nullable=False),
    sa.Column('code_phrase', sa.String(), nullable=False),
    sa.Column('secret_key', sa.String(), nullable=False),
    sa.Column('date_of_creation', sa.DateTime(), nullable=True),
    sa.Column('TTL', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_secrets_id'), 'secrets', ['id'], unique=False)
    op.create_index(op.f('ix_secrets_secret'), 'secrets', ['secret'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_secrets_secret'), table_name='secrets')
    op.drop_index(op.f('ix_secrets_id'), table_name='secrets')
    op.drop_table('secrets')
    # ### end Alembic commands ###
