import enum
import uuid  # noqa

from db import db
from db.models.account import Account
from sqlalchemy_utils.types import UUIDType  # noqa


class RoleType(enum.Enum):
    LEAD_ASSESSOR = "Lead Assessor"
    ASSESSOR = "Assessor"
    COMMENTER = "Commenter"


class Role(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    account_id = db.Column(
        "account_id",
        UUIDType(binary=False),
        db.ForeignKey(Account.id),
    )
    role = db.Column(
        "role",
        db.Enum(RoleType),
        nullable=False,
    )
