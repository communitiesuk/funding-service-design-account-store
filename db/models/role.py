import uuid  # noqa

from sqlalchemy.dialects.postgresql import UUID

from db import db
from db.models.account import Account


class Role(db.Model):
    id = db.Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    account_id = db.Column(
        "account_id",
        UUID(as_uuid=True),
        db.ForeignKey(Account.id),
    )
    role = db.Column(
        "role",
        db.String(),
        nullable=False,
    )
