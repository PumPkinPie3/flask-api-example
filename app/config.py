import os


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask-api-example_development'.format(**{
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'host': os.getenv('MYSQL_HOST', 'localhost'),
    })

    SQLALCHEMY_POOL_SIZE = 15
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SALT = 'HAKATANOSIO'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask-api-example_production'.format(**{
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'host': os.getenv('MYSQL_HOST'),
    })


class StagingConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask-api-example_staging'.format(**{
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'host': os.getenv('MYSQL_HOST', 'localhost'),
    })


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask-api-example_test'.format(**{
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'host': os.getenv('MYSQL_HOST', 'localhost'),
    })


config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'test': TestConfig
}
