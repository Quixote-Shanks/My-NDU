"""add foriegn key to posts table

Revision ID: 9086403fccc6
Revises: 74c33b0cb0d4
Create Date: 2022-12-22 14:53:02.707601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9086403fccc6'
down_revision = '74c33b0cb0d4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user-fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_pk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
