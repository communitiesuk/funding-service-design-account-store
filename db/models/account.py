import uuid  # noqa

from db import db
from fsd_utils.authentication.utils import get_highest_role
from sqlalchemy.dialects.postgresql import UUID


class Account(db.Model):

    id = db.Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
    )
    email = db.Column("email", db.String(), nullable=False, unique=True)
    full_name = db.Column("full_name", db.String(), nullable=True)
    azure_ad_subject_id = db.Column(
        "azure_ad_subject_id", db.String(), nullable=True, unique=True
    )
    roles = db.relationship(
        "Role", lazy="select", backref=db.backref("account", lazy="joined")
    )

    @property
    def highest_role(self):
        return get_highest_role([role.role for role in self.roles])
