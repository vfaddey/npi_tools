"""cascade_card_delete

Revision ID: dd71fc42176f
Revises: 4c2c7aff36d8
Create Date: 2025-02-09 16:44:10.272105

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dd71fc42176f"
down_revision: Union[str, None] = "4c2c7aff36d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "card_copies_card_id_fkey", "card_copies", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "card_copies", "cards", ["card_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint(
        "sharing_urls_card_id_fkey", "sharing_urls", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "sharing_urls", "cards", ["card_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "sharing_urls", type_="foreignkey")
    op.create_foreign_key(
        "sharing_urls_card_id_fkey",
        "sharing_urls",
        "cards",
        ["card_id"],
        ["id"],
    )
    op.drop_constraint(None, "card_copies", type_="foreignkey")
    op.create_foreign_key(
        "card_copies_card_id_fkey", "card_copies", "cards", ["card_id"], ["id"]
    )
    # ### end Alembic commands ###
