"""create raw data table

Revision ID: 1a4e129f239b
Revises: 3fc2d3abbb0b
Create Date: 2016-05-08 14:50:14.971956

"""

# revision identifiers, used by Alembic.
import datetime
revision = '1a4e129f239b'
down_revision = '3fc2d3abbb0b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import LONGTEXT


def upgrade():
    op.create_table(
        'raw_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_ts', sa.TIMESTAMP(), default=datetime.datetime.utcnow),
        sa.Column('updated_ts', sa.TIMESTAMP(), onupdate=datetime.datetime.utcnow),
        sa.Column('domain', sa.String(length=100), nullable=False, index=True),
        sa.Column('url', sa.String(length=255), nullable=False),
        sa.Column('depth', sa.SMALLINT(), nullable=False),
        sa.Column('http_status', sa.String(3), nullable=True, index=True),
        sa.Column('html', LONGTEXT(), nullable=True),
        sa.Column('parsed_as_entry', sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url'),
        mysql_charset='utf8',
        mysql_engine='InnoDB'
    )
    pass


def downgrade():
    op.drop_table('raw_data')
    pass
