"""create domain table

Revision ID: 3fc2d3abbb0b
Revises: 157951f7c315
Create Date: 2016-05-08 10:07:33.982632

"""

# revision identifiers, used by Alembic.
import datetime
revision = '3fc2d3abbb0b'
down_revision = '157951f7c315'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'domain',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('domain', sa.String(length=100), nullable=False),
        sa.Column('spider_name', sa.String(length=60), nullable=True),
        sa.Column('article_num', sa.Integer(), nullable=True),
        sa.Column('created_ts', sa.TIMESTAMP(), default=datetime.datetime.utcnow),
        sa.Column('updated_ts', sa.TIMESTAMP(), onupdate=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('domain'),
        mysql_charset='utf8',
        mysql_engine='InnoDB'
    )
    pass


def downgrade():
    op.drop_table('domain')
    pass
