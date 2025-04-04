"""file_hash

Revision ID: fe02030f43d3
Revises: 5c45ba18a583
Create Date: 2025-01-23 14:14:37.536866

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe02030f43d3"
down_revision: Union[str, None] = "5c45ba18a583"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cards", "group_id", existing_type=sa.UUID(), nullable=False
    )
    op.add_column(
        "files", sa.Column("file_hash", sa.String(length=64), nullable=True)
    )
    op.create_index(
        op.f("ix_files_file_hash"), "files", ["file_hash"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_files_file_hash"), table_name="files")
    op.drop_column("files", "file_hash")
    op.alter_column(
        "cards", "group_id", existing_type=sa.UUID(), nullable=True
    )
    # ### end Alembic commands ###
