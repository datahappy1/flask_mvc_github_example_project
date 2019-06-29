import os
from flask import Blueprint, request, flash, redirect
from github import GithubException
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
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

        model_gh.File.save_file(global_variables.obj,
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
        model_gh.File.save_file(global_variables.obj,
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
        model_gh.File.delete_file(global_variables.obj,
                                  gh_file_path=file_name,
                                  message=message,
                                  branch_name=branch_name)
        flash(f'{file_name} deletion was committed to the repository branch {branch_name} '
              f'with the message {message}!', category="success")

        return redirect('/views/gh_files_manager/branch/'+branch_name)


def session_getter() -> list:
    try:
        session_id = []
        github_session_id = model_gh.Model.get_session_id(global_variables.obj)
        session_id.append(str(github_session_id))
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'session_getter(), '
                f'exception: {str(ge)}']
    return session_id


def branch_lister() -> list:
    try:
        branch_list = model_gh.Branch.list_all_branches(global_variables.obj)
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'branch_lister(), '
                f'exception: {str(ge)}']
    return branch_list


def file_lister(branch_name) -> list:
    try:
        _files_list = model_gh.File.list_all_files(global_variables.obj, branch_name)
        files_list = []
        for file in _files_list:
            file_extension = os.path.splitext(str(file))[1]
            if file_extension in settings.editable_file_extensions_list:
                files_list.append([file, True])
            else:
                files_list.append([file, False])
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'file_lister({branch_name}), '
                f'exception: {str(ge)}']
    return files_list


def file_exists_checker(gh_file_path, branch_name) -> list:
    try:
        file_status = []
        github_file_status = model_gh.File.get_file_status(global_variables.obj, gh_file_path, branch_name)
        file_status.append(github_file_status)
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'file_exists_checker({gh_file_path},{branch_name}),'
                f'exception: {str(ge)}']
    return file_status


def file_content_getter(gh_file_path, branch_name) -> list:
    try:
        file_content = []
        github_file_content = model_gh.File.get_file_contents(global_variables.obj, gh_file_path, branch_name)
        file_content.append(github_file_content)
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'file_exists_checker({gh_file_path},{branch_name}), '
                f'exception: {str(ge)}']
    return file_content
