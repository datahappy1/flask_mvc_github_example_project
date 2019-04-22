import os
from flask import Flask, render_template, request, redirect
from flaskr.lib import gh, settings

# github related variables
token = os.environ['token']
# branch_name and local_file_path is temporary for testing
repo = settings.repo
branch_name = "dev"
local_file_path = os.getcwd().rstrip('lib') + os.path.join('\\files', 'temp', 'test_' + branch_name + '.json')

# init the github class
obj = gh.GitHubClass(init_token=token, init_repo=repo, init_branch_name=branch_name,
                     init_local_file_path=local_file_path)

# flask app starts here
app = Flask(__name__)

# https://www.tutorialspoint.com/flask/flask_templates.htm
# http://flask.pocoo.org/docs/1.0/tutorial/layout/


@app.route('/')
def index():
    return render_template('index.html')


# https://stackoverflow.com/questions/45877080/how-to-create-dropdown-menu-from-python-list-using-flask-and-html


@app.route('/config')
def config():
    gh_session_id = gh.GitHubClass.get_session_id(obj)
    b_list = gh.GitHubClass.list_all_branches(obj)
    f_list = gh.GitHubClass.list_all_files(obj)

    return render_template('config.html', gh_session_id=gh_session_id,
                           b_list=b_list, curr_branch=branch_name, f_list=f_list)

# https://www.tutorialspoint.com/flask/flask_file_uploading.htm
# https://www.roytuts.com/python-flask-file-upload-example/
# https://stackoverflow.com/questions/42424853/saving-upload-in-flask-only-saves-to-project-root
# TODO /upload like a extension of the config template


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.abspath(os.path.dirname(__file__))+'', f.filename)

        return redirect('/config')


@app.route('/workflow')
def workflow():
    return render_template('workflow.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
