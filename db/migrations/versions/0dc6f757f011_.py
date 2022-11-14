"""empty message

Revision ID: 0dc6f757f011
Revises: 13d601bfaee1
Create Date: 2022-11-12 08:13:12.206935

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils # noqa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '0dc6f757f011'
down_revision = '13d601bfaee1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        role = postgresql.ENUM('ADMIN', 'LEAD_ASSESSOR', 'ASSESSOR', 'COMMENTER', 'APPLICANT', name='role')
        role.create(op.get_bind())

        batch_op.add_column(sa.Column('role', role, server_default='APPLICANT', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('role')

        bind = op.get_bind()
        sa.Enum(name='role').drop(bind, checkfirst=False)

    # ### end Alembic commands ###
