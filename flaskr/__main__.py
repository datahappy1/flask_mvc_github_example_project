import os
from flask import Flask, render_template, request, redirect, flash
from flaskr.lib import gh, settings
from flaskr.controllers import gh_files as gh_files

# project related variables
local_temp_files_path = settings.local_temp_files_path

# github related variables
token = os.environ['github_token']
repo = settings.repo
repo_folder = settings.repo_folder
init_branch_name = settings.initial_branch_name

# init the github class
obj = gh.GitHubClass(init_token=token, init_repo=repo)

# flask app starts here
app = Flask(__name__)
app.secret_key = os.environ['flask_secret_key']


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
    files_list = gh.GitHubClass.list_all_files(obj, branch_name)

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_current_branch=branch_name,
                           template_file_list=files_list)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/put', methods=['GET'])
def upload(branch_name):
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


# blueprint as import from models
@app.route('/uploader/<branch_name>/', methods=['GET', 'POST'])
def uploader(branch_name):
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        message = request.form['commit_message']
        f.save(local_temp_files_path + filename)
        flash(filename + ' was stored!', category="success")

        with open(local_temp_files_path + f.filename, 'rb') as f:
            file_contents = f.read()

        gh.GitHubClass.create_file(obj, path="flaskr/files_playground/" + filename, message=message,
                                   content=file_contents, branch_name=branch_name)
        flash(f'{filename} was committed to the repository with the message {message}!', category="success")

        if os.path.isfile(local_temp_files_path + filename):
            os.remove(local_temp_files_path + filename)

        return redirect('/views/gh_files_manager/branch/'+branch_name)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/post/<file_name>', methods=['GET'])
def edit(branch_name, file_name):
    return render_template('views/file_editor.html',
                           template_current_branch=branch_name,
                           file_name=file_name)


# blueprint as import from models
@app.route('/editor/<branch_name>/<file_name>', methods=['GET', 'POST'])
def editor(branch_name, file_name):
    return redirect('index.html')


@app.route('/views/gh_files_manager/branch/<branch_name>/file/delete/<file_name>', methods=['GET'])
def delete(branch_name, file_name):
    return render_template('views/file_editor.html',
                           template_current_branch=branch_name,
                           file_name=file_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)