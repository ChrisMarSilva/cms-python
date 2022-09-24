"""alteracao no campo email para 100 chars na tabela pessoa

Revision ID: 3c1ee6056ce3
Revises: c357afe11b1c
Create Date: 2022-07-29 13:51:34.047691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c1ee6056ce3'
down_revision = 'c357afe11b1c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('pessoa', 'email', existing_type=sa.VARCHAR(length=50), type_=sa.String(length=100), existing_nullable=False)
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.alter_column('email', existing_type=sa.VARCHAR(length=50), type_=sa.String(length=100), existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('pessoa', 'email', existing_type=sa.String(length=100), type_=sa.VARCHAR(length=50), existing_nullable=False)
    with op.batch_alter_table('pessoa', schema=None) as batch_op:
        batch_op.alter_column('email', existing_type=sa.String(length=100), type_=sa.VARCHAR(length=50), existing_nullable=False)
    # ### end Alembic commands ###