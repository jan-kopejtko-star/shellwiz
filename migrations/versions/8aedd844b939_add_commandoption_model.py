"""Add CommandOption model

Revision ID: 8aedd844b939
Revises: 3c574284ec93
Create Date: 2025-03-15 14:34:41.890966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aedd844b939'
down_revision = '3c574284ec93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('command_options',
    sa.Column('option_id', sa.Integer(), nullable=False),
    sa.Column('command_id', sa.Integer(), nullable=True),
    sa.Column('flag', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['command_id'], ['commands.command_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('option_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('command_options')
    # ### end Alembic commands ###
