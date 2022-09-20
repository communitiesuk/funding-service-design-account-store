from db import db
from db.models.account import Account
from sqlalchemy import ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint


class AccountApplicationRelationship(db.Model):

    account_id = db.Column(ForeignKey(Account.id))
    application_id = db.Column(
        "application_id", db.String(), nullable=False, primary_key=True
    )
    __table_args__ = (PrimaryKeyConstraint("account_id", "application_id"),)
