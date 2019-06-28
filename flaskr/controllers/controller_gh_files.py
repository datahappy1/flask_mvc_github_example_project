import os
from flask import Blueprint, request, flash, redirect
from github import GithubException
from flaskr.lib import github, global_variables
from tempfile import NamedTemporaryFile

controller_gh_files = Blueprint('controller_gh_files', __name__, template_folder='templates')


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


def session_getter() -> list:
    try:
        session_id = []
        github_session_id = github.GitHubClass.get_session_id(global_variables.obj)
        session_id.append(str(github_session_id))
    except GithubException as ge:
        return ['Github Exception', f'raised in function {str(__name__)}.branch_lister, exception: {str(ge)}']
    return session_id


def branch_lister() -> list:
    try:
        branch_list = github.GitHubClass.list_all_branches(global_variables.obj)
    except GithubException as ge:
        return ['Github Exception', f'raised in function {str(__name__)}.branch_lister, exception: {str(ge)}']
    return branch_list


def file_lister(branch_name) -> list:
    try:
        files_list = github.GitHubClass.list_all_files(global_variables.obj, branch_name)

    except GithubException as ge:
        return ['Github Exception', f'raised in function {str(__name__)}.file_lister, exception: {str(ge)}']
    return files_list


def file_exists_checker(gh_file_path, branch_name) -> list:
    try:
        file_status = []
        github_file_status = github.GitHubClass.get_file_status(global_variables.obj, gh_file_path, branch_name)
        file_status.append(github_file_status)
    except GithubException as ge:
        return ['Github Exception', f'raised in function {str(__name__)}.file_exists_checker, exception: {str(ge)}']
    return file_status


def file_content_getter(gh_file_path, branch_name) -> list:
    try:
        file_content = []
        github_file_content = github.GitHubClass.get_file_contents(global_variables.obj, gh_file_path, branch_name)
        file_content.append(github_file_content)
    except GithubException as ge:
        return ['Github Exception', f'raised in function {str(__name__)}.file_exists_checker, exception: {str(ge)}']
    return file_content
