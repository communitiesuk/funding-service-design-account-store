"""empty message

Revision ID: d7ec79e76cf0
Revises: e355f9c4356b
Create Date: 2023-06-22 15:26:02.972151

"""

import sqlalchemy as sa
import sqlalchemy_utils  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d7ec79e76cf0"
down_revision = "e355f9c4356b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("role", sa.Column("new_role", sa.String(), nullable=True))
    op.execute(
        "UPDATE role SET new_role = CASE role "
        "WHEN 'LEAD_ASSESSOR' THEN 'COF_LEAD_ASSESSOR' "
        "WHEN 'ASSESSOR' THEN 'COF_ASSESSOR' "
        "WHEN 'COMMENTER' THEN 'COF_COMMENTER' END"
    )
    op.drop_column("role", "role")
    op.alter_column("role", "new_role", new_column_name="role", nullable=False)


def downgrade():
    op.add_column(
        "role",
        sa.Column(
            "new_role",
            sa.Enum("LEAD_ASSESSOR", "ASSESSOR", "COMMENTER", name="roletype"),
            nullable=True,
        ),
    )
    op.execute(
        "UPDATE role SET new_role = CASE role "
        "WHEN 'COF_LEAD_ASSESSOR' THEN 'LEAD_ASSESSOR'::roletype "
        "WHEN 'COF_ASSESSOR' THEN 'ASSESSOR'::roletype "
        "WHEN 'COF_COMMENTER' THEN 'COMMENTER'::roletype END"
    )
    op.drop_column("role", "role")
    op.alter_column("role", "new_role", new_column_name="role", nullable=False)
