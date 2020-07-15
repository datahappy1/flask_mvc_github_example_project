"""
main project file
"""
from flask import render_template, jsonify, request
from flaskr import APP, settings


@APP.errorhandler(405)
def not_allowed(error):
    """
    not allowed method error handler function
    :param error:
    :return:error html page or api response
    """
    if request.path.startswith(settings.API_BASE_ENDPOINT):
        response = jsonify({
            'status': 405,
            'error': str(error),
            'mimetype': 'application/json'
        })
        response.status_code = 405
        return response
    return render_template('error_page.html', template_error_message=error)


@APP.errorhandler(404)
def not_found(error):
    """
    not found app error handler function
    :param error:
    :return:error html page or api response
    """
    if request.path.startswith(settings.API_BASE_ENDPOINT):
        response = jsonify({
            'status': 404,
            'error': str(error),
            'mimetype': 'application/json'
        })
        response.status_code = 404
        return response
    return render_template('error_page.html', template_error_message=error)


@APP.route('/')
def index():
    """
    index route render template function
    :return:
    """
    return render_template('index.html',
                           template_current_branch=settings.INITIAL_BRANCH_NAME)


if __name__ == '__main__':
    APP.run(debug=True, host='127.0.0.1', threaded=True)
