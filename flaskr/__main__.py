"""
main project file
"""
import os

from flask import Flask, render_template, jsonify, request
from flaskr.project_variables import settings, global_variables
from flaskr.models import model_gh
from flaskr.controllers.controller_gh_ui import CONTROLLER_GH_UI
# you can also import specific functions from a Blueprint module:
# from flaskr.controllers.common_functions import session_getter, branch_lister, file_lister
from flaskr.controllers.controller_gh_api import CONTROLLER_GH_API


def create_app():
    """
    create app factory pattern
    :return:
    """
    # flask app starts here
    _app = Flask(__name__)
    _app.secret_key = os.environ['flask_secret_key']
    _app.register_blueprint(CONTROLLER_GH_UI)
    _app.register_blueprint(CONTROLLER_GH_API)
    return _app


APP = create_app()

# github related variables
TOKEN = os.environ['github_token']

# init the github class
global_variables.OBJ = model_gh.Model(init_token=TOKEN,
                                      init_repo=settings.REPO)


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
