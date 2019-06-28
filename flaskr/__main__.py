import os.path

from flask import Flask, render_template, redirect, flash
from flaskr.lib import github, settings, global_variables
from flaskr.controllers.controller_gh_files import controller_gh_files
from flaskr.controllers.controller_gh_files import session_getter, branch_lister, \
    file_lister, file_exists_checker, file_content_getter

# project related variables

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


@app.route('/views/gh_files_manager/branch/<branch_name>', methods=['GET', 'POST'])
def gh_files_manager(branch_name):
    gh_session_id = session_getter()[0]
    if gh_session_id == "Github Exception":
        flash('{}, {}'.format(gh_session_id[0], (gh_session_id[1])), category="warning")
        return redirect('/')

    branch_list = branch_lister()
    if branch_list[0] == "Github Exception":
        flash('{}, {}'.format(branch_list[0],(branch_list[1])), category="warning")
        return redirect('/')

    files_list = file_lister(branch_name)
    if files_list[0] == "Github Exception":
        flash('{}, {}'.format(files_list[0],(files_list[1])), category="warning")
        return redirect('/')

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_current_branch=branch_name,
                           template_file_list=files_list)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/put', methods=['GET'])
def upload(branch_name):
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/post/<path:file_name>', methods=['GET'])
def edit(branch_name, file_name):
    file_status_code = file_exists_checker(gh_file_path=file_name, branch_name=branch_name)[0]
    if file_status_code == 200:
        file_contents = file_content_getter(gh_file_path=file_name, branch_name=branch_name)[0]
        return render_template('views/file_editor.html',
                               template_current_branch=branch_name,
                               file_name=file_name,
                               file_contents=file_contents)
    elif file_status_code == "Github Exception":
        flash('{}, {}'.format(file_status_code[0], (file_status_code[1])), category="warning")
        return redirect('/views/gh_files_manager/branch/' + branch_name)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/delete/<path:file_name>', methods=['GET'])
def delete(branch_name, file_name):
    file_status_code = file_exists_checker(gh_file_path=file_name, branch_name=branch_name)[0]
    if file_status_code == 200:
        return render_template('views/file_deleter.html',
                               template_current_branch=branch_name,
                               file_name=file_name)
    elif file_status_code == "Github Exception":
        flash('{}, {}'.format(file_status_code[0], (file_status_code[1])), category="warning")
        return redirect('/views/gh_files_manager/branch/' + branch_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
