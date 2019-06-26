import os.path
from flask import Flask, render_template
from flaskr.lib import github, settings, global_variables
from flaskr.controllers.controller_gh_files import controller_gh_files
from flaskr.lib.exceptions.exception_decor import exception
from flaskr.lib.exceptions.exception_logger import create_logger

# project related variables


# setup logging
logger = create_logger()


# github related variables
token = os.environ['github_token']
repo = settings.repo
repo_folder = settings.repo_folder
init_branch_name = settings.initial_branch_name

# init the github class
global_variables.obj = github.GitHubClass(init_token=token, init_repo=repo)

# flask app starts here
app = Flask(__name__)
app.secret_key = os.environ['flask_secret_key']
app.register_blueprint(controller_gh_files)


@app.route('/')
def index():
    return render_template('index.html',
                           template_current_branch=init_branch_name)


@app.route('/error_page')
def error_page(error_message):
    return render_template('error_page.html',
                           template_error_message=error_message)


@exception(logger)
@app.route('/views/gh_files_manager/branch/<branch_name>', methods=['GET', 'POST'])
def gh_files_manager(branch_name):
    gh_session_id = github.GitHubClass.get_session_id(global_variables.obj)
    branch_list = github.GitHubClass.list_all_branches(global_variables.obj)
    files_list = github.GitHubClass.list_all_files(global_variables.obj, branch_name)

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_current_branch=branch_name,
                           template_file_list=files_list)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/put', methods=['GET'])
def upload(branch_name):
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


@exception(logger)
@app.route('/views/gh_files_manager/branch/<branch_name>/file/post/<path:file_name>', methods=['GET'])
def edit(branch_name, file_name):
    try:
        gh_file = github.GitHubClass.get_file_contents(global_variables.obj, file_name, branch_name)
    except Exception as e:
        return render_template('error_page.html',
                               error_message=f'File {file_name} not found, exception: {str(e)}')

    file_status_code, file_contents = gh_file[0], gh_file[1]

    if file_status_code == 200:
        return render_template('views/file_editor.html',
                               template_current_branch=branch_name,
                               file_name=file_name,
                               file_contents=file_contents)
    else:
        return render_template('error_page.html',
                               error_message=f'File {file_name} not found, github response status: {str(file_status_code)}')


@exception(logger)
@app.route('/views/gh_files_manager/branch/<branch_name>/file/delete/<path:file_name>', methods=['GET'])
def delete(branch_name, file_name):
    try:
        gh_file = github.GitHubClass.get_file_contents(global_variables.obj, file_name, branch_name)
    except Exception as e:
        return render_template('error_page.html',
                               error_message=f'File {file_name} not found, exception: {str(e)}')

    file_status_code, file_contents = gh_file[0], gh_file[1]

    if file_status_code == 200:
        return render_template('views/file_deleter.html',
                               template_current_branch=branch_name,
                               file_name=file_name,
                               file_contents=file_contents)
    else:
        return render_template('error_page.html',
                               error_message=f'File {file_name} not found, github response status: {str(file_status_code)}')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)