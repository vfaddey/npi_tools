"""card_null_result

Revision ID: 12e1f36024f2
Revises: a9d6815fe87c
Create Date: 2025-02-28 10:02:44.982292

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "12e1f36024f2"
down_revision: Union[str, None] = "a9d6815fe87c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cards",
        "result",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cards",
        "result",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )
    # ### end Alembic commands ###
