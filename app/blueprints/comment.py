from flask import request, jsonify, abort, Blueprint, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import Post, Comment


app = Blueprint('comment', __name__)


def to_comment(params):
    user_id = params['user_id']
    text = params['title']
    return user_id, text


def get_data(post_id):
    try:
        post = Post.query.filter_by(id=post_id).one()
        comment = Comment.query.filter_by(post_id=post.id).all()
        return comment
    except NoResultFound as e:
        title = '[PostNotFound]'
        message = 'Post {} is not found.'.format(post_id)
        current_app.logger.error(title + message)
        abort(400, {'title': title, 'message': message})


def add_data(post_id, params):
    try:
        user_id, text = to_comment(params)
        comment = Comment(user_id=user_id, post_id=post_id, text=text)

        db.session.add(comment)
        db.session.commit()
        return comment

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        abort(500, str(e))


def delete_data(comment_id):
    try:
        comment = Comment.query.filter_by(comment_id=comment_id).one()
        comment.query.delete()
        db.session.commit()

    except NoResultFound as e:
        title = '[CommentNotFound]'
        message = 'Comment {} is not found.'.format(comment_id)
        current_app.logger.error(title + message)
        abort(400, {'title': title, 'message': message})

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        abort(500, str(e))


@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comment(post_id):
    comment = get_data(post_id)
    rv = comment.to_dict()
    return jsonify(rv)


@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    comments = add_data(post_id, request.get_json())
    rv = [c.to_dict() for c in comments]
    return jsonify(rv)


@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    delete_data(comment_id)
    return jsonify()
