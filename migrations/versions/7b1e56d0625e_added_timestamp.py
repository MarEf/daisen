"""added timestamp

Revision ID: 7b1e56d0625e
Revises: 6edd2c078053
Create Date: 2023-01-23 20:17:05.954450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b1e56d0625e'
down_revision = '6edd2c078053'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('applicationDate', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.drop_column('applicationDate')

    # ### end Alembic commands ###
