"""update article table

Revision ID: 5503e038121a
Revises: 4e2eb2538333
Create Date: 2016-04-16 10:52:26.563420

"""

# revision identifiers, used by Alembic.
revision = '5503e038121a'
down_revision = '4e2eb2538333'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('article', 'published_ts')
    op.add_column('article', sa.Column('published_ts', sa.TIMESTAMP(), nullable=True))
    op.drop_column('article', 'url')
    op.add_column('article', sa.Column('url', sa.String(length=255), nullable=False))
    op.create_unique_constraint("url", "article", ["url"])
    op.add_column('article', sa.Column('site_unique_id', sa.String(length=10), nullable=True))
    op.add_column('article', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('article', sa.Column('author_email', sa.String(length=30), nullable=True))
    op.add_column('article', sa.Column('author_phone', sa.String(length=12), nullable=True))
    op.add_column('article', sa.Column('author_role', sa.String(length=20), nullable=True))
    op.add_column('article', sa.Column('cover_real_url', sa.String(length=255), nullable=True))
    op.add_column('article', sa.Column('source_type', sa.String(length=30), nullable=True))
    op.add_column('article', sa.Column('views_count', sa.Integer(), nullable=True))
    op.add_column('article', sa.Column('cover', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('article', 'published_ts')
    op.add_column('article', sa.Column('published_ts', sa.Text(), nullable=True))
    op.drop_column('article', 'url')
    op.add_column('article', sa.Column('url', sa.String(length=25), nullable=False))
    op.create_unique_constraint("url", "article", ["url"])
    op.drop_column('article', 'site_unique_id')
    op.drop_column('article', 'author_id')
    op.drop_column('article', 'author_email')
    op.drop_column('article', 'author_phone')
    op.drop_column('article', 'author_role')
    op.drop_column('article', 'cover_real_url')
    op.drop_column('article', 'source_type')
    op.drop_column('article', 'views_count')
    op.drop_column('article', 'cover')
