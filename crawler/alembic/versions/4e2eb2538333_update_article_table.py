"""update article table

Revision ID: 4e2eb2538333
Revises: 3bf61fe1e092
Create Date: 2016-04-14 00:23:27.417959

"""

# revision identifiers, used by Alembic.
revision = '4e2eb2538333'
down_revision = '3bf61fe1e092'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('article', sa.Column('summary', sa.Text(), nullable=True))
    op.add_column('article', sa.Column('published_ts', sa.Text(), nullable=True))
    op.add_column('article', sa.Column('author_avatar', sa.String(255), nullable=True))
    pass


def downgrade():
    op.drop_column('article', 'summary')
    op.drop_column('article', 'published_ts')
    op.drop_column('article', 'author_avatar')
    pass
