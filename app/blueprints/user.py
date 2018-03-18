from hashlib import sha256
from flask import request, jsonify, abort, Blueprint, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import User


app = Blueprint('user', __name__)


def get_data(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        return user
    except NoResultFound as e:
        title = '[UserNotFound]'
        message = 'User {} is not found.'.format(user_id)
        current_app.logger.error(title + message)
        abort(400, {'title': title, 'message': message})


def add_data(params):
    try:
        name, password, email = to_user(params)
        user = User(name=name, password=password, email=email)

        db.session.add(user)
        db.session.commit()
        return user

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        abort(500, str(e))


def delete_data(user_id):
    try:
        user = get_data(user_id)
        user.query.delete()
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        abort(500, str(e))


def to_user(params):
    name = params['name']
    password = params['password']
    email = params['email']
    return name, hash(password), email


def hash(password):
    p = password + current_app.config['SALT']
    m = sha256(p.encode('utf-8')).hexdigest()
    return m


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_data(user_id)
    rv = user.to_dict()
    return jsonify(rv)


@app.route('/users', methods=['POST'])
def add_user():
    user = add_data(request.get_json())
    rv = user.to_dict()
    return jsonify(rv)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    delete_data(user_id)
    return jsonify()
