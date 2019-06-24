import os
from flask import Blueprint, request, flash, redirect
from flaskr.lib import github, global_variables

controller_gh_files = Blueprint('controller_gh_files', __name__, template_folder='templates')


@controller_gh_files.route('/uploader/<branch_name>/', methods=['GET', 'POST'])
def uploader(branch_name):
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        message = request.form['commit_message']
        f.save(global_variables.local_temp_files_path + filename)
        flash(filename + ' was stored!', category="success")
        with open(global_variables.local_temp_files_path + f.filename, 'rb') as f:
            file_contents = f.read()

        github.GitHubClass.create_file(global_variables.obj, path="flaskr/files_playground/" + filename, message=message,
                                       content=file_contents, branch_name=branch_name)
        flash(f'{filename} was committed to the repository with the message {message}!', category="success")
        if os.path.isfile(global_variables.local_temp_files_path + filename):
            os.remove(global_variables.local_temp_files_path + filename)

        return redirect('/views/gh_files_manager/branch/'+branch_name)


@controller_gh_files.route('/editor/<branch_name>/<path:file_name>', methods=['GET', 'POST'])
def editor(branch_name, file_name):
    return redirect('index.html')


@controller_gh_files.route('/deleter/<branch_name>/<path:file_name>', methods=['GET', 'POST'])
def deleter(branch_name, file_name):
    return redirect('index.html')
