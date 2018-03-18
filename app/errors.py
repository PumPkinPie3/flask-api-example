from flask import request, jsonify


def error_handler(app):
    @app.errorhandler(404)
    def not_found(error):
        response = jsonify({
            'title': '[NotFound]',
            'details': 'The requested URL {} was not found '.format(request.path)
        })
        return response, error.code

    @app.errorhandler(400)
    @app.errorhandler(500)
    def base(error):
        response = jsonify({
            'title': error.description['title'],
            'details': error.description['message']
        })
        return response, error.code

