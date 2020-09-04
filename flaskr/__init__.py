"""
__init__.py
"""
import os
from flask import Flask
from flaskr import settings
from flaskr.models.model_gh import GhBaseModel
from flaskr.controllers.controller_gh_ui import CONTROLLER_GH_UI
from flaskr.controllers.controller_gh_api import CONTROLLER_GH_API


def create_app():
    """
    create app factory pattern
    :return:
    """
    current_app = Flask(__name__)
    current_app.secret_key = os.environ['flask_secret_key']

    current_app.register_blueprint(CONTROLLER_GH_UI)
    current_app.register_blueprint(CONTROLLER_GH_API)

    current_app.config['model_github'] = GhBaseModel(init_token=os.environ['github_token'],
                                                     init_repo=settings.REPO)
    return current_app


APP = create_app()
