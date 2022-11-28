import uuid  # noqa

from db import db
from sqlalchemy_utils.types import UUIDType  # noqa


class Account(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
    )
    email = db.Column("email", db.String(), nullable=False, primary_key=True)
    full_name = db.Column("full_name", db.String(), nullable=True)
    roles = db.relationship(
        "Role", lazy="select", backref=db.backref("account", lazy="joined")
    )

    @property
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "roles": [role.role.name for role in self.roles],
        }
