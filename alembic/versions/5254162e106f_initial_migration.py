"""Initial migration

Revision ID: 5254162e106f
Revises: 
Create Date: 2023-07-29 12:41:51.428035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5254162e106f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stockbatchinfo', sa.Column('batch_num', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stockbatchinfo', 'batch_num')
    # ### end Alembic commands ###
