"""Initial migration

Revision ID: 4446c6c71ad9
Revises: 4d6501441683
Create Date: 2025-04-15 10:13:55.749763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4446c6c71ad9'
down_revision: Union[str, None] = '4d6501441683'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.alter_column('posts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('posts', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('posts', 'body',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'body',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('posts', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('posts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###
