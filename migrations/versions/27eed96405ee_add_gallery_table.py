"""add_gallery_table

Revision ID: 27eed96405ee
Revises: b0ef77c130de
Create Date: 2023-03-10 04:57:51.586655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27eed96405ee'
down_revision = 'b0ef77c130de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('galleries',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=2048), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gallery_id', sa.BigInteger(), nullable=False))
        batch_op.create_foreign_key(None, 'galleries', ['gallery_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('gallery_id')

    op.drop_table('galleries')
    # ### end Alembic commands ###
