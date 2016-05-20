"""add index for created_ts and updated_ts

Revision ID: 3d4fa0558243
Revises: 1a4e129f239b
Create Date: 2016-05-20 00:19:43.494978

"""

# revision identifiers, used by Alembic.
revision = '3d4fa0558243'
down_revision = '1a4e129f239b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('created_ts', 'article', ['created_ts'])
    op.create_index('updated_ts', 'article', ['updated_ts'])
    pass


def downgrade():
    op.drop_index('created_ts', table_name='article')
    op.drop_index('updated_ts', table_name='article')
    pass
