import os.path
from flask import Flask, render_template
from flaskr.lib import settings, global_variables
from flaskr.models import model_gh
from flaskr.controllers.controller_gh_webapp import controller_gh_webapp
# you can also import specific functions from a Blueprint module:
# from flaskr.controllers.utils import session_getter, branch_lister, file_lister
from flaskr.controllers.controller_gh_api import controller_gh_api

# flask app starts here
app = Flask(__name__)
app.secret_key = os.environ['flask_secret_key']
app.register_blueprint(controller_gh_webapp)
app.register_blueprint(controller_gh_api)


# github related variables
token = os.environ['github_token']

# init the github class
global_variables.obj = model_gh.Model(init_token=token, init_repo=settings.repo)


@app.route('/')
def index():
    return render_template('index.html',
                           template_current_branch=settings.initial_branch_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
