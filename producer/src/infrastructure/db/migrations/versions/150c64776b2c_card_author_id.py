"""card_author_id

Revision ID: 150c64776b2c
Revises: 86edd3c27244
Create Date: 2025-02-05 01:58:14.477387

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "150c64776b2c"
down_revision: Union[str, None] = "86edd3c27244"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("cards", sa.Column("author_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_cards_author_id"), "cards", ["author_id"], unique=False
    )
    op.create_foreign_key(None, "cards", "users", ["author_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "cards", type_="foreignkey")
    op.drop_index(op.f("ix_cards_author_id"), table_name="cards")
    op.drop_column("cards", "author_id")
    # ### end Alembic commands ###
