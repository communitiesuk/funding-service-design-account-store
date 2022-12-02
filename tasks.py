from colored import attr
from colored import fg
from colored import stylize
from invoke import task

ECHO_STYLE = fg("blue") + attr("bold")
DB_NAME = "fsd_account_store_dev"


@task
def bootstrap_dev_db(c, database_host="localhost"):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {DB_NAME}")
    print(stylize(f"{DB_NAME} db dropped...", ECHO_STYLE))
    c.run(f"createdb -h {database_host} {DB_NAME}")
    print(stylize(f"{DB_NAME} db created...", ECHO_STYLE))
