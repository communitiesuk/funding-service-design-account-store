from contextlib import contextmanager
import os
from uuid import uuid4
from colored import attr
from colored import fg
from colored import stylize
from invoke import task
from app import app as connexionapp
from db.models.account import Account
from sqlalchemy import select
from db.models.role import Role  # noqa:E402

ECHO_STYLE = fg("blue") + attr("bold")
DB_NAME = "fsd_account_store_dev"


@contextmanager
def _env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


@task
def bootstrap_dev_db(c, database_host="localhost"):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {DB_NAME}")
    print(stylize(f"{DB_NAME} db dropped...", ECHO_STYLE))
    c.run(f"createdb -h {database_host} {DB_NAME}")
    print(stylize(f"{DB_NAME} db created...", ECHO_STYLE))


@task
def seed_local_account_store(c):
    with _env_var("FLASK_ENV", "development"):
        with connexionapp.app.app_context():
            from db import db

            LEAD_ASSESSOR = "lead_assessor@example.com"
            lead_assessor_account = (
                db.session.query(Account)
                .where(Account.email == LEAD_ASSESSOR)
                .one_or_none()
            )
            if not lead_assessor_account:
                # Create account
                account_id = uuid4()
                lead_assessor_account = Account(id=account_id, email=LEAD_ASSESSOR)
                db.session.add(lead_assessor_account)
                db.session.commit()
                print("Created lead assessor account")
            else:
                print("Lead assessor account already exists")
                account_id = lead_assessor_account.id

            lead_assessor_roles = db.session.scalars(
                select(Role.role).where(Role.account_id == account_id)
            ).all()

            roles_to_add = []

            for required_role in [
                "CTDF_LEAD_ASSESSOR",
                "CTDF_ASSESSOR",
                "CTDF_COMMENTER",
            ]:
                if required_role not in lead_assessor_roles:
                    la_role = Role(
                        id=uuid4(), account_id=account_id, role=required_role
                    )
                    roles_to_add.append(la_role)
                    print(f"Creating role {required_role} for lead assessor")

            db.session.bulk_save_objects(roles_to_add)
            db.session.commit()
