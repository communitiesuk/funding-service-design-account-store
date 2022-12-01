from db import ma
from db.models.role import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True

    role = ma.auto_field()
