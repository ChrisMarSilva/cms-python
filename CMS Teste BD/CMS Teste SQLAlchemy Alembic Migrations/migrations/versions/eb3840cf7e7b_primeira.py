"""primeira

Revision ID: eb3840cf7e7b
Revises: 
Create Date: 2022-07-19 21:51:01.017219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb3840cf7e7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pessoa',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=50), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('pessoa')
