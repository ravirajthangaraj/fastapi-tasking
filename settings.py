import os

ENV = os.environ.get('TASKING_ENV', 'dev')

print(f"TASKING_ENV - {ENV}")


def read_config():
    configuration = {}
    try:
        import config
        for setting in dir(config):
            if not setting.startswith('__'):
                configuration.update({setting: getattr(config, setting)})
    except ImportError as e:
        print(e)
    return configuration


if ENV == 'dev':
    environ = read_config()
else:
    environ = os.environ

SECRET_KEY = environ['SECRET_KEY']

DATABASE_CLASS = 'app.database.mongo'
DATABASE_URL = environ['DATABASE_URL']
DATABASE_USERNAME = environ['DATABASE_USERNAME']
DATABASE_PASSWORD = environ['DATABASE_PASSWORD']
DATABASE_NAME = environ['DATABASE_NAME']
DATABASE_URL_TEST = environ['DATABASE_URL_TEST']
DATABASE_USERNAME_TEST = environ['DATABASE_USERNAME_TEST']
DATABASE_PASSWORD_TEST = environ['DATABASE_PASSWORD_TEST']
DATABASE_NAME_TEST = environ['DATABASE_NAME_TEST']
