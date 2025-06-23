"""Merge heads

Revision ID: f3c85992b792
Revises: 7b71e1adf162, 97f48ea08bfc
Create Date: 2025-06-23 17:41:54.052062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3c85992b792'
down_revision: Union[str, None] = ('7b71e1adf162', '97f48ea08bfc')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
