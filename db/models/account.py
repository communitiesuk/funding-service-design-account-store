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
    email = db.Column("email", db.String(), nullable=False, unique=True)
    full_name = db.Column("full_name", db.String(), nullable=True)
    azure_ad_subject_id = db.Column(
        "azure_ad_subject_id", db.String(), nullable=True, unique=True
    )
    roles = db.relationship(
        "Role", lazy="select", backref=db.backref("account", lazy="joined")
    )
