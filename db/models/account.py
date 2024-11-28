import uuid  # noqa
from typing import Mapping

from flask import current_app
from fsd_utils.authentication.utils import get_highest_role_map
from sqlalchemy.dialects.postgresql import UUID

from db import db


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
    def highest_role_map(self) -> Mapping[str, str]:
        roles_as_strings = [r.role for r in self.roles]
        role_map = get_highest_role_map(roles_as_strings)
        current_app.logger.debug(f"Role map for {self.id}: {role_map}")
        return role_map
