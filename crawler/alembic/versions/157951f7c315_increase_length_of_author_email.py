"""increase length of author_email

Revision ID: 157951f7c315
Revises: 5503e038121a
Create Date: 2016-05-01 10:44:50.365591

"""

# revision identifiers, used by Alembic.
revision = '157951f7c315'
down_revision = '5503e038121a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('article', 'author_email', type_=sa.String(50), nullable=True)
    op.alter_column('article', 'author_name', type_=sa.String(30), nullable=True)
    pass


def downgrade():
    op.alter_column('article', 'author_email', type_=sa.String(30), nullable=True)
    op.alter_column('article', 'author_name', type_=sa.String(15), nullable=True)
    pass
