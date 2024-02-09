from marshmallow import fields

from db import ma
from db.models.account import Account


class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account

    id = fields.UUID(data_key="account_id")
    email = fields.String(data_key="email_address")
    full_name = ma.auto_field()
    azure_ad_subject_id = ma.auto_field()
    roles = ma.Function(lambda obj: [role.role for role in obj.roles])
    highest_role_map = ma.Function(lambda obj: obj.highest_role_map)
