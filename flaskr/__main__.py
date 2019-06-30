import os.path

from flask import Flask, render_template
from flaskr.lib import settings, global_variables
from flaskr.models import model_gh
from flaskr.controllers.controller_gh import controller_gh
# you can also import from Blueprint specific functions:
# from flaskr.controllers.controller_gh import session_getter, branch_lister, file_lister

# flask app starts here
app = Flask(__name__)
app.secret_key = os.environ['flask_secret_key']
app.register_blueprint(controller_gh)

# github related variables
token = os.environ['github_token']
repo = settings.repo
repo_folder = settings.repo_folder
init_branch_name = settings.initial_branch_name

# init the github class
global_variables.obj = model_gh.Model(init_token=token, init_repo=repo)


@app.route('/')
def index():
    return render_template('index.html',
                           template_current_branch=init_branch_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
