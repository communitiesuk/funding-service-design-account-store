from db import db
from db.models.account import Account
from sqlalchemy import ForeignKey


class AccountApplicationRelationship(db.Model):

    account_id = db.Column("id", ForeignKey(Account.id))
    application_id = db.Column(
        "application_id", db.String(), nullable=False, primary_key=True
    )
