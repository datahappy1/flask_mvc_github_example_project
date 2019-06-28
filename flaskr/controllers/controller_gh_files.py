import os
from flask import Blueprint, request, flash, redirect
from flaskr.lib import github, global_variables, settings
from tempfile import NamedTemporaryFile

controller_gh_files = Blueprint('controller_gh_files', __name__, template_folder='templates')


@controller_gh_files.route('/file_lister/<branch_name>/', methods=['GET', 'POST'])
def file_lister(branch_name):
    pass


@controller_gh_files.route('/uploader/<branch_name>/', methods=['GET', 'POST'])
def uploader(branch_name):
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        message = request.form['commit_message']

        temp_file_handler = NamedTemporaryFile(delete=False)
        temp_file_path = temp_file_handler.name
        temp_file_handler.write(bytes(file))

        flash(file_name + ' was stored!', category="success")
        with open(temp_file_path, 'rb') as f:
            file_contents = f.read()

        github.GitHubClass.save_file(global_variables.obj,
                                     gh_file_path="flaskr/files_playground/" + file_name,
                                     message=message,
                                     content=file_contents,
                                     branch_name=branch_name)

        os.unlink(temp_file_path)
        assert not os.path.exists(temp_file_path)

        flash(f'{file_name} was committed to the repository branch {branch_name} '
              f'with the message {message}!', category="success")

        return redirect('/views/gh_files_manager/branch/'+branch_name)


@controller_gh_files.route('/editor/<branch_name>/file/post/<path:file_name>', methods=['GET', 'POST'])
def editor(branch_name, file_name):
    if request.method == 'POST':
        file_contents = request.form['file_contents']

        message = request.form['commit_message']
        github.GitHubClass.save_file(global_variables.obj,
                                     gh_file_path=file_name,
                                     message=message,
                                     content=file_contents,
                                     branch_name=branch_name)
        flash(f'{file_name} update was committed to the repository branch {branch_name} '
              f'with the message {message}!', category="success")

        return redirect('/views/gh_files_manager/branch/'+branch_name)


@controller_gh_files.route('/deleter/<branch_name>/file/delete/<path:file_name>', methods=['GET', 'POST'])
def deleter(branch_name, file_name):
    if request.method == 'POST':
        message = request.form['commit_message']
        github.GitHubClass.delete_file(global_variables.obj,
                                       gh_file_path=file_name,
                                       message=message,
                                       branch_name=branch_name)
        flash(f'{file_name} deletion was committed to the repository branch {branch_name} '
              f'with the message {message}!', category="success")

        return redirect('/views/gh_files_manager/branch/'+branch_name)
