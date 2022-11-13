import uuid  # noqa

from db import db
from sqlalchemy_utils.types import UUIDType  # noqa


import enum


class Role(enum.Enum):
    LEAD_ASSESSOR = "Lead Assessor"
    ASSESSOR = "Assessor"
    COMMENTER = "Commenter"
    APPLICANT = "Applicant"


class Account(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    email = db.Column("email", db.String(), nullable=False, primary_key=True)
    role = db.Column("role", db.Enum(Role), nullable=False, default=Role.APPLICANT.name, server_default=Role.APPLICANT.name)
