from core.dumb_data_store import dummmy_db_connection

if True:

    db_connection = dummmy_db_connection()

else:

    db_connection = "a real connection"
