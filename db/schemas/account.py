from db import ma
from db.models.account import Account
from fsd_utils.authentication.utils import get_highest_role
from marshmallow import fields


class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account

    id = fields.UUID(data_key="account_id")
    email = fields.String(data_key="email_address")
    full_name = ma.auto_field()
    azure_ad_subject_id = ma.auto_field()
    roles = ma.Function(lambda obj: [role.role.name for role in obj.roles])
    highest_role = ma.Function(lambda obj: obj.highest_role)
