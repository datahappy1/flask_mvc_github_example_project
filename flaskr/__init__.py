import os
from flask import Flask
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
    app = Flask(__name__)
    app.secret_key = os.environ['flask_secret_key']
    app.register_blueprint(CONTROLLER_GH_UI)
    app.register_blueprint(CONTROLLER_GH_API)

    # init the github class
    global_variables.GH_OBJ = model_gh.Model(init_token=os.environ['github_token'],
                                             init_repo=settings.REPO)

    return app


APP = create_app()
