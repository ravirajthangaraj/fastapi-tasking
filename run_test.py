import pytest
import os

import settings
os.environ.setdefault('UNIT_TESTING', '1')

from app.database.mongo import db

from app.database.db_helper import drop_database


db.database = settings.DATABASE_NAME_TEST
db.connect()

test = pytest.main(['-v', '--html=test_report/report.html'])
os.environ.setdefault('UNIT_TESTING', '0')
drop_database()
