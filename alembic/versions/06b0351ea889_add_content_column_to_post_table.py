"""add content column to post table

Revision ID: 06b0351ea889
Revises: c8c419e6308c
Create Date: 2022-12-22 14:38:59.212943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06b0351ea889'
down_revision = 'c8c419e6308c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
