from marshmallow import fields
from marshmallow.fields import Function
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field

from db.models.account import Account


class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account

    id = fields.UUID(data_key="account_id")
    email = fields.String(data_key="email_address")
    full_name = auto_field()
    azure_ad_subject_id = auto_field()
    roles = Function(lambda obj: [role.role for role in obj.roles])
    highest_role_map = Function(lambda obj: obj.highest_role_map)
