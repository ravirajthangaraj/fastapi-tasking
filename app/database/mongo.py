import os
import uuid

import pymongo
import settings
from app.database.database import Database


class MongoDB(Database):
    client = None
    database = None

    def __init__(self, database_url, database_name, *args, **kwargs):
        self.database_url = database_url
        self.database_name = database_name

    def connect(self, *args, **kwargs):
        self.client = pymongo.MongoClient(self.database_url)
        try:
            self.database = self.client[self.database_name]
        except Exception as e:
            print(e)

    def drop_database(self):
        try:
            self.client.drop_database(self.database_name)
        except Exception as e:
            print(e)
            return False
        return True

    def create(self, collection_name, document: dict):
        document.update({'fuid': uuid.uuid4().hex})
        result = self.database[collection_name].insert_one(document)
        return result

    def get(self, collection_name, query, *args, **kwargs):
        kwargs.setdefault('exclude_fields', {})
        exclude_fields = {}
        exclude_fields.update(kwargs.get('exclude_fields'))

        result = self.database[collection_name].find(query, exclude_fields)
        return result

    def retrieve(self, collection_name, query, *args, **kwargs):
        kwargs.setdefault('exclude_fields', {})
        exclude_fields = {}
        exclude_fields.update(kwargs.get('exclude_fields'))

        result = self.database[collection_name].find_one(query, exclude_fields)
        return result


try:
    if os.environ.get('UNIT_TESTING', '0') == '1':
        db = MongoDB(settings.DATABASE_URL_TEST, settings.DATABASE_NAME_TEST)
        db.connect()
    else:
        db = MongoDB(settings.DATABASE_URL, settings.DATABASE_NAME)
        db.connect()

except Exception as e:
    print(e)
    print(f"Connection to database was unsuccessful")
    exit(-1)
