import os.path

from flask import Flask, render_template, redirect, flash
from flaskr.lib import settings, global_variables
from flaskr.models import model_gh
from flaskr.controllers.controller_gh import controller_gh
from flaskr.controllers.controller_gh import session_getter, \
    branch_lister, branch_deleter, file_lister, file_exists_checker, file_content_getter

# project related variables

# github related variables
token = os.environ['github_token']
repo = settings.repo
repo_folder = settings.repo_folder
init_branch_name = settings.initial_branch_name

# init the github class
global_variables.obj = model_gh.Model(init_token=token, init_repo=repo)

# flask app starts here
app = Flask(__name__)
app.secret_key = os.environ['flask_secret_key']
app.register_blueprint(controller_gh)


@app.route('/')
def index():
    return render_template('index.html',
                           template_current_branch=init_branch_name)


@app.route('/views/gh_branches_manager/', methods=['GET', 'POST'])
def gh_branches_manager():
    gh_session_id = session_getter()[0]
    if str(gh_session_id).startswith("Github Exception"):
        flash('{}'.format(gh_session_id), category="warning")
        return redirect('/')

    branch_list = branch_lister()
    if str(branch_list[0]).startswith("Github Exception"):
        flash('{}'.format(str(branch_list[0])), category="warning")
        return redirect('/')

    return render_template('views/gh_branches_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_repo=repo)


@app.route('/views/gh_branches_manager/branch/post/<branch_name>/', methods=['GET'])
def create_branch(branch_name):
    return render_template('views/branch_creator.html',
                           template_current_branch=branch_name)


@app.route('/views/gh_branches_manager/branch/<branch_name>/delete/', methods=['GET'])
def delete_branch(branch_name):
    branch_status_code = 200
    if branch_status_code == 200:
        return render_template('views/branch_deleter.html',
                               template_current_branch=branch_name)
    elif str(branch_status_code).startswith("Github Exception"):
        flash('{}'.format(branch_status_code), category="warning")
        return redirect('/views/gh_branches_manager/')


@app.route('/views/gh_files_manager/branch/<branch_name>/', methods=['GET', 'POST'])
def gh_files_manager(branch_name):
    gh_session_id = session_getter()[0]
    if str(gh_session_id).startswith("Github Exception"):
        flash('{}'.format(gh_session_id), category="warning")
        return redirect('/')

    branch_list = branch_lister()
    if str(branch_list[0]).startswith("Github Exception"):
        flash('{}'.format(str(branch_list[0])), category="warning")
        return redirect('/')

    files_list = file_lister(branch_name)
    if str(files_list[0]).startswith("Github Exception"):
        flash('{}'.format(str(files_list[0])), category="warning")
        return redirect('/')

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_current_branch=branch_name,
                           template_file_list=files_list)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/post/', methods=['GET'])
def upload_file(branch_name):
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/put/<path:file_name>', methods=['GET'])
def edit_file(branch_name, file_name):
    file_status_code = file_exists_checker(gh_file_path=file_name, branch_name=branch_name)[0]
    if file_status_code == 200:
        file_contents = file_content_getter(gh_file_path=file_name, branch_name=branch_name)[0]
        return render_template('views/file_editor.html',
                               template_current_branch=branch_name,
                               file_name=file_name,
                               file_contents=file_contents)
    elif str(file_status_code).startswith("Github Exception"):
        flash('{}'.format(file_status_code), category="warning")
        return redirect('/views/gh_files_manager/branch/' + branch_name)


@app.route('/views/gh_files_manager/branch/<branch_name>/file/delete/<path:file_name>', methods=['GET'])
def delete_file(branch_name, file_name):
    file_status_code = file_exists_checker(gh_file_path=file_name, branch_name=branch_name)[0]
    if file_status_code == 200:
        return render_template('views/file_deleter.html',
                               template_current_branch=branch_name,
                               file_name=file_name)
    elif str(file_status_code).startswith("Github Exception"):
        flash('{}'.format(file_status_code), category="warning")
        return redirect('/views/gh_files_manager/branch/' + branch_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
