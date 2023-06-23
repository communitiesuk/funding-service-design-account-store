import uuid  # noqa
from typing import Mapping

from db import db
from flask import current_app
from sqlalchemy.dialects.postgresql import UUID


_ROLE_HIERARCHY = [
    "LEAD_ASSESSOR",
    "ASSESSOR",
    "COMMENTER",
]


def _fund_short_name_to_highest_role_map(roles: list[str]) -> Mapping[str, str]:
    roles_with_fund_prefix = tuple(f"_{rh}" for rh in _ROLE_HIERARCHY)
    filtered_roles = [r for r in roles if r.endswith(roles_with_fund_prefix)]

    fund_short_name_to_roles_list = {}
    for role in filtered_roles:
        fund_short_name, sub_role = role.split("_", 1)
        if fund_short_name in fund_short_name_to_roles_list:
            fund_short_name_to_roles_list[fund_short_name].append(sub_role)
        else:
            fund_short_name_to_roles_list[fund_short_name] = [sub_role]

    fund_short_name_to_highest_role = {}
    for fund_short_name, roles_list in fund_short_name_to_roles_list.items():
        highest_role, *_ = sorted(roles_list, key=lambda x: _ROLE_HIERARCHY.index(x))
        fund_short_name_to_highest_role[fund_short_name] = highest_role

    return fund_short_name_to_highest_role


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
        role_map = _fund_short_name_to_highest_role_map(roles_as_strings)
        current_app.logger.debug(f"Role map for {self.id}: {role_map}")
        return role_map
