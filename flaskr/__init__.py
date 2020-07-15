"""
__init__.py
"""
import os
from flask import Flask
from flaskr import settings
from flaskr.models.model_global import MODEL_GLOBAL_DICT
from flaskr.models.model_gh import GhBaseModel
from flaskr.controllers.controller_gh_ui import CONTROLLER_GH_UI
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

    MODEL_GLOBAL_DICT['github'] = GhBaseModel(init_token=os.environ['github_token'],
                                              init_repo=settings.REPO)

    return app


APP = create_app()
