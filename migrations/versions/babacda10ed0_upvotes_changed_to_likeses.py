"""upvotes changed to likeses

Revision ID: babacda10ed0
Revises: 2f4f9efa803c
Create Date: 2022-12-08 20:18:09.733437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'babacda10ed0'
down_revision = '2f4f9efa803c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=True))
        batch_op.drop_column('upVotes')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upVotes', sa.INTEGER(), nullable=True))
        batch_op.drop_column('likes')

    # ### end Alembic commands ###
