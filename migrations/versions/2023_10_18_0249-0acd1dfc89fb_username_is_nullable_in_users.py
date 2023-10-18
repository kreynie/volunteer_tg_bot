"""username is nullable in users

Revision ID: 0acd1dfc89fb
Revises: b802cc4fa11d
Create Date: 2023-10-18 02:49:59.471980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0acd1dfc89fb"
down_revision: Union[str, None] = "b802cc4fa11d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###
