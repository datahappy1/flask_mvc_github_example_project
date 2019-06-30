import os
from flask import Blueprint, request, flash, redirect, render_template
from flask_restful import Resource, Api
from github import GithubException
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from werkzeug.utils import secure_filename

controller_gh = Blueprint('controller_gh', __name__, template_folder='templates')


# @controller_gh.routes for reads from the model - functions returning redirects

@controller_gh.route('/views/gh_branches_manager/', methods=['GET'])
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
                           template_repo_name=settings.repo)


@controller_gh.route('/views/gh_branches_manager/branch/post/<branch_name>/', methods=['GET'])
def create_branch(branch_name):
    return render_template('views/branch_creator.html',
                           template_current_branch=branch_name)


@controller_gh.route('/views/gh_branches_manager/branch/<branch_name>/delete/', methods=['GET'])
def delete_branch(branch_name):
    branch_status_code = 200
    if branch_status_code == 200:
        return render_template('views/branch_deleter.html',
                               template_current_branch=branch_name)
    elif str(branch_status_code).startswith("Github Exception"):
        flash('{}'.format(branch_status_code), category="warning")
        return redirect('/views/gh_branches_manager/')


@controller_gh.route('/views/gh_files_manager/branch/<branch_name>/', methods=['GET'])
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


@controller_gh.route('/views/gh_files_manager/branch/<branch_name>/file/post/', methods=['GET'])
def upload_file(branch_name):
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


@controller_gh.route('/views/gh_files_manager/branch/<branch_name>/file/put/<path:file_name>', methods=['GET'])
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


@controller_gh.route('/views/gh_files_manager/branch/<branch_name>/file/delete/<path:file_name>', methods=['GET'])
def delete_file(branch_name, file_name):
    file_status_code = file_exists_checker(gh_file_path=file_name, branch_name=branch_name)[0]
    if file_status_code == 200:
        return render_template('views/file_deleter.html',
                               template_current_branch=branch_name,
                               file_name=file_name)
    elif str(file_status_code).startswith("Github Exception"):
        flash('{}'.format(file_status_code), category="warning")
        return redirect('/views/gh_files_manager/branch/' + branch_name)


# @controller_gh.routes for writes to the model - functions accepting form requests and returning redirects
@controller_gh.route('/branch_creator/src/<branch_name_src>/', methods=['GET', 'POST'])
def branch_creator(branch_name_src):
    if request.method == 'POST':
        branch_name_tgt = request.form['branch_name_tgt']
        branch_name_tgt = str(branch_name_tgt).replace(' ','')
        model_gh.Branch.create_branch(global_variables.obj,
                                      source_branch=branch_name_src,
                                      target_branch=branch_name_tgt)
        flash(f'branch {branch_name_tgt} based on {branch_name_src} was created!', category="success")

        return redirect('/views/gh_branches_manager/')


@controller_gh.route('/branch_deleter/<branch_name>/', methods=['GET', 'POST'])
def branch_deleter(branch_name):
    if request.method == 'POST':
        model_gh.Branch.delete_branch(global_variables.obj,
                                      branch_name=branch_name)
        flash(f'branch {branch_name} was deleted!', category="success")

        return redirect('/views/gh_branches_manager/')


@controller_gh.route('/file_uploader/<branch_name>/', methods=['GET', 'POST'])
def file_uploader(branch_name):
    if request.method == 'POST':
        if request.files:
            file = request.files['uploaded_file']
            message = request.form['commit_message']

            file_name = secure_filename(file.filename)
            temp_file_path = os.path.join(os.getcwd(), 'temp', file_name)
            file.save(temp_file_path)

            with open(temp_file_path, 'rb') as temp_file_handler:
                file_contents = temp_file_handler.read()

            model_gh.File.create_file(global_variables.obj,
                                      gh_file_path="flaskr/" + settings.repo_folder + file_name,
                                      message=message,
                                      content=file_contents,
                                      branch_name=branch_name)

            flash(f'file {file_name} was committed to the repository branch {branch_name} '
                  f'with the message {message}!', category="success")

            os.unlink(temp_file_path)
            assert not os.path.exists(temp_file_path)
        else:
            flash('No file uploaded', category="warning")

        return redirect('/views/gh_files_manager/branch/'+branch_name)


@controller_gh.route('/file_editor/<branch_name>/file/put/<path:file_name>', methods=['GET', 'POST'])
def file_editor(branch_name, file_name):
    if request.method == 'POST':
        file_contents = request.form['file_contents']

        message = request.form['commit_message']
        model_gh.File.update_file(global_variables.obj,
                                  gh_file_path=file_name,
                                  message=message,
                                  content=file_contents,
                                  branch_name=branch_name)
        flash(f'file {file_name} update was committed to the repository branch {branch_name} '
              f'with the message {message}!', category="success")

        return redirect('/views/gh_files_manager/branch/'+branch_name)


@controller_gh.route('/file_deleter/<branch_name>/file/delete/<path:file_name>', methods=['GET', 'POST'])
def file_deleter(branch_name, file_name):
    if request.method == 'POST':
        message = request.form['commit_message']
        model_gh.File.delete_file(global_variables.obj,
                                  gh_file_path=file_name,
                                  message=message,
                                  branch_name=branch_name)
        flash(f'file {file_name} deletion was committed to the repository branch {branch_name} '
              f'with the message {message}!', category="success")

        return redirect('/views/gh_files_manager/branch/'+branch_name)


# controller helper functions returning values only
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

