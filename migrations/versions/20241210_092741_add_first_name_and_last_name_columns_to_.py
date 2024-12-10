"""Add first_name and last_name columns to users table

Revision ID: 2c7bec91f139
Revises: 0fc2be32b00d
Create Date: 2024-12-10 09:27:41.857552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c7bec91f139'
down_revision = '0fc2be32b00d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=25), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=25), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###
