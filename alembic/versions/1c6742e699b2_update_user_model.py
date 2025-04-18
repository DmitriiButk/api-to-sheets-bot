"""update User model

Revision ID: 1c6742e699b2
Revises: 21073d72dc6c
Create Date: 2025-04-15 11:25:49.117601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c6742e699b2'
down_revision: Union[str, None] = '21073d72dc6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('catch_phrase', sa.String(), nullable=False))
    op.drop_column('company', 'catchPhrase')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('catchPhrase', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('company', 'catch_phrase')
    # ### end Alembic commands ###
