
class Config(object):
    ENV_NAME = 'None'
    LOG_FILE = 'app.log'

    # random_id()
    LOGIN_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:main@localhost/main_dev'

class DevConfig(Config):
    SQLALCHEMY_RECORD_QUERIES = True
    ENV_NAME = 'Dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:main@localhost/main_dev'

class TestConfig(Config):
    SERVER_NAME = 'localhost:5005'
    SQLALCHEMY_RECORD_QUERIES = True
    ENV_NAME = 'Test'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:main@localhost/main_test'

class QAConfig(Config):
    SQLALCHEMY_RECORD_QUERIES = True
    ENV_NAME = 'QA'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:main@localhost/main_test'

class ProdConfig(Config):
    ENV_NAME = 'Prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://main:main@localhost/main_test'
