import os
from flask import Flask, render_template, request, redirect, flash
from flaskr.lib import gh, settings
from flaskr.controllers import gh_files as controller

# project related variables
local_temp_files_path = settings.local_temp_files_path

# github related variables
token = os.environ['token']
repo = settings.repo
repo_folder = settings.repo_folder
init_branch_name = settings.initial_branch_name

# init the github class
obj = gh.GitHubClass(init_token=token, init_repo=repo, init_branch_name=init_branch_name)

# flask app starts here
app = Flask(__name__)
app.secret_key = 'abcd1234'


@app.route('/')
def index():
    return render_template('index.html',
                           template_current_branch=init_branch_name)


@app.route('/error_page')
def error_page(error_message):
    return render_template('error_page.html',
                           template_error_message=error_message)


@app.route('/views/gh_files_manager/branch/<branch_name>', methods=['GET', 'POST'])
def gh_files_manager(branch_name):
    gh_session_id = gh.GitHubClass.get_session_id(obj)
    branch_list = gh.GitHubClass.list_all_branches(obj)
    files_list = gh.GitHubClass.list_all_files(obj)

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_current_branch=branch_name,
                           template_file_list=files_list)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/put', methods=['GET'])
def upload(branch_name):
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


@app.route('/uploader/<branch_name>/', methods=['GET', 'POST'])
def uploader(branch_name):
    if request.method == 'POST':
        f = request.files['file']
        message = request.form['commit_message']
        f.save(local_temp_files_path + f.filename)
        flash(f.filename + ' was stored!', category="success")

        with open(local_temp_files_path + f.filename, 'rb') as f:
            file_contents = f.read()

        gh.GitHubClass.create_file(obj, path="/", message=message, content=file_contents)
        flash(f.filename + ' was committed!', category="success")

        os.path.isfile(local_temp_files_path + f.filename)

        return redirect('/views/gh_files_manager/branch/'+branch_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
    #import model and controller as blueprints