import os


class Config(object):
    DEBUG = False
    TESTING = False

    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'flask-api-example_development')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(**{
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
        'host': MYSQL_HOST,
        'database': MYSQL_DATABASE
    })

    SQLALCHEMY_POOL_SIZE = 15
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SALT = 'HAKATANOSIO'


class ProductionConfig(Config):
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(**{
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
        'host': MYSQL_HOST,
        'database': MYSQL_DATABASE
    })


class StagingConfig(Config):
    DEBUG = True

    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(**{
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
        'host': MYSQL_HOST,
        'database': MYSQL_DATABASE
    })


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True

    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'flask-api-example_test')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(**{
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
        'host': MYSQL_HOST,
        'database': MYSQL_DATABASE
    })


config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'test': TestConfig
}
