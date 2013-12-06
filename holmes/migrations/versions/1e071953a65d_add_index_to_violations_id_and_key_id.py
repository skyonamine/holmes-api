"""add_index_to_violations_id_and_key_id

Revision ID: 1e071953a65d
Revises: 2f32c106a437
Create Date: 2013-12-05 23:53:53.303743

"""

# revision identifiers, used by Alembic.
revision = '1e071953a65d'
down_revision = '2f32c106a437'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('idx_violations_id_key_id', 'violations', ['key_id', 'id'])


def downgrade():
    op.drop_index('idx_violations_id_key_id', 'violations')

