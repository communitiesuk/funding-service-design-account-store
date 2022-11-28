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
    roles = db.relationship(
        "Role", lazy="select", backref=db.backref("account", lazy="joined")
    )

    @property
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "roles": [role.role.name for role in self.roles],
        }
