"""create article table

Revision ID: 3bf61fe1e092
Revises: 
Create Date: 2016-04-11 17:59:03.776116

"""

# revision identifiers, used by Alembic.
revision = '3bf61fe1e092'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'article',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=25), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_ts', sa.TIMESTAMP(), nullable=True),
        sa.Column('updated_ts', sa.TIMESTAMP(), nullable=True),
        sa.Column('time_str', sa.String(20), nullable=True, doc='readable time from the page'),
        sa.Column('author_name', sa.String(15), nullable=True),
        sa.Column('author_link', sa.String(255), nullable=True),
        sa.Column('tags', sa.String(60), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url'),
        mysql_charset='utf8',
        mysql_engine='InnoDB'
    )
    pass


def downgrade():
    op.drop_table('article')
    pass
