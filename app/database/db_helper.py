from app.database.mongo import db


def drop_database(database_name=None):
    try:
        if database_name:
            db.client.drop_database(database_name)
        else:
            db.drop_database()
    except Exception as e:
        print(e)
