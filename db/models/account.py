import uuid  # noqa

from db import db
from sqlalchemy_utils.types import UUIDType  # noqa


class Account(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    email = db.Column("email", db.String(), nullable=False, primary_key=True)
