"""add user table

Revision ID: 74c33b0cb0d4
Revises: 06b0351ea889
Create Date: 2022-12-22 14:44:09.195171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74c33b0cb0d4'
down_revision = '06b0351ea889'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
