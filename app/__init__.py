import os
from decimal import Decimal
from datetime import datetime

from flask import Flask, request
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config
from .log import Log
from .errors import error_handler

db = SQLAlchemy()
log = Log()


def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    db.init_app(app)
    log.init_app(app)

    Migrate(app, db)

    register_blueprints(app)
    register_teardowns(app)
    register_error_handler(app)
    register_cli(app)

    app.json_encoder = CustomJSONEncoder

    return app


def register_blueprints(app):
    from .blueprints.user import app as user
    from .blueprints.post import app as post
    from .blueprints.comment import app as comment

    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(comment)


def register_teardowns(app):
    @app.teardown_request
    def access_logger(e):
        if e is not None:
            app.logger.error(e)

        app.logger.info(request)

    @app.teardown_appcontext
    def close_db(e):
        if e is not None:
            app.logger.error(e)
        db.session.close()


def register_error_handler(app):
    error_handler(app)


def register_cli(app):
    import click
    from sqlalchemy import create_engine

    @app.cli.command(short_help='Create databases')
    def create_db():
        uri, database = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)
        mysql_engine = create_engine(uri)
        mysql_engine.execute('CREATE DATABASE IF NOT EXISTS `{}`;'.format(database))
        click.echo('Create {} in {}'.format(database, uri.rsplit('@', 1)[1]))


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return JSONEncoder.default(self, obj)
