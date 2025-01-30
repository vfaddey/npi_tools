"""card_copies

Revision ID: 86edd3c27244
Revises: 246a430b12bb
Create Date: 2025-01-30 14:15:50.635498

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "86edd3c27244"
down_revision: Union[str, None] = "246a430b12bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "card_copies",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("card_id", sa.UUID(), nullable=False),
        sa.Column("copier_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["card_id"],
            ["cards.id"],
        ),
        sa.ForeignKeyConstraint(
            ["copier_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_card_copies_card_id"),
        "card_copies",
        ["card_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_card_copies_copier_id"),
        "card_copies",
        ["copier_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_card_copies_copier_id"), table_name="card_copies")
    op.drop_index(op.f("ix_card_copies_card_id"), table_name="card_copies")
    op.drop_table("card_copies")
    # ### end Alembic commands ###
