import os
from decimal import Decimal
from datetime import datetime
from flask import Flask, request
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from .config import config
from .log import Log
from .errors import error_handler
from .clis import cli_handler

db = SQLAlchemy()
log = Log()


def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    db.init_app(app)
    log.init_app(app)

    register_blueprints(app)
    register_teardowns(app)
    register_error_handler(app)
    register_cli_handler(app)

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


def register_cli_handler(app):
    cli_handler(app)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return JSONEncoder.default(self, obj)
