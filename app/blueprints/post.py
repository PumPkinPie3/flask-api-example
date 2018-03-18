from flask import request, jsonify, abort, Blueprint, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import Post

app = Blueprint('post', __name__)


def to_post(params):
    user_id = params['user_id']
    title = params['title']
    body = params['body']
    return user_id, title, body


def get_data(post_id):
    try:
        post = Post.query.filter_by(id=post_id).one()
        return post
    except NoResultFound as e:
        title = '[PostNotFound]'
        message = 'Post {} is not found.'.format(post_id)
        current_app.logger.error(title + message)
        abort(400, {'title': title, 'message': message})


def add_data(params):
    try:
        user_id, title, body = to_post(params)
        post = Post(user_id=user_id, title=title, body=body)

        db.session.add(post)
        db.session.commit()
        return post

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        abort(500, str(e))


def delete_data(post_id):
    try:
        post = get_data(post_id)
        post.query.delete()
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        abort(500, str(e))


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = get_data(post_id)
    rv = post.to_dict()
    return jsonify(rv)


@app.route('/posts', methods=['POST'])
def add_post():
    post = add_data(request.get_json())
    rv = post.to_dict()
    return jsonify(rv)


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    delete_data(post_id)
    return jsonify()
