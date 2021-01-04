"""empty message

Revision ID: e95d2352c5ac
Revises: e93908c0c43f
Create Date: 2021-01-03 21:00:21.329675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e95d2352c5ac'
down_revision = 'e93908c0c43f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currency', sa.Column('code', sa.String(length=8), nullable=False))
    op.add_column('currency', sa.Column('name', sa.String(length=64), nullable=False))
    op.create_index(op.f('ix_currency_code'), 'currency', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_currency_code'), table_name='currency')
    op.drop_column('currency', 'name')
    op.drop_column('currency', 'code')
    # ### end Alembic commands ###
