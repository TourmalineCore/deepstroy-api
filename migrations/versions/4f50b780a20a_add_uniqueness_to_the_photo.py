"""add_uniqueness_to_the_photo

Revision ID: 4f50b780a20a
Revises: 3073e2c41eb6
Create Date: 2023-04-19 03:38:48.468691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f50b780a20a'
down_revision = '3073e2c41eb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('color_uniqueness', sa.SmallInteger(), nullable=True))
        batch_op.add_column(sa.Column('tag_uniqueness', sa.SmallInteger(), nullable=True))
        batch_op.add_column(sa.Column('overall_uniqueness', sa.SmallInteger(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.drop_column('overall_uniqueness')
        batch_op.drop_column('tag_uniqueness')
        batch_op.drop_column('color_uniqueness')

    # ### end Alembic commands ###