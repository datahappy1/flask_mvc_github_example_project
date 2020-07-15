"""
controller github ui module
"""
import os

from flask import Blueprint, request, flash, redirect, render_template, abort
from werkzeug.exceptions import BadRequestKeyError

from flaskr import settings, utils
from flaskr.controllers import common_functions

CONTROLLER_GH_UI = Blueprint('controller_gh_ui', __name__, template_folder='templates')
GH_FILE_PATH_BASE = "flaskr/" + settings.REPO_FOLDER


@CONTROLLER_GH_UI.route('/gh_branches_manager/', methods=['GET'])
def gh_branches_manager():
    """
    github branches manager function
    :return:
    """
    _session_id_response_ui = common_functions.session_getter()
    gh_session_status, gh_session_id = _session_id_response_ui.get('status'), \
                                       _session_id_response_ui.get('content')
    flash(f'PyGithub connect success {gh_session_status}, {gh_session_id}', category="success")

    _branch_list_response_ui = common_functions.branch_lister()
    branch_list_status = _branch_list_response_ui.get('status')

    if branch_list_status == 200:
        branch_list_content = _branch_list_response_ui.get('content')
        flash(f'Branches load success {branch_list_status}', category="success")
    else:
        branch_list_error = _branch_list_response_ui.get('error')
        flash(f'Branches load exception {branch_list_error}', category="danger")
        return redirect('/')

    return render_template('views/gh_branches_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list_content,
                           template_repo_name=settings.REPO)


@CONTROLLER_GH_UI.route('/gh_branches_manager/branch/<branch_name>/create/',
                        methods=['GET', 'POST'])
def create_branch(branch_name):
    """
    create branch function
    :param branch_name:
    :return:
    """
    if request.method == "GET":
        return render_template('views/branch_creator.html',
                               template_current_branch=branch_name)

    if request.method == "POST":
        branch_name_src_ui = request.form['branch_name_src']
        branch_name_tgt_ui = request.form['branch_name_tgt']
        _branch_create_response_ui = common_functions.branch_creator(branch_name_src_ui,
                                                                     branch_name_tgt_ui)
        branch_create_status = _branch_create_response_ui.get('status')

        if branch_create_status == 201:
            flash(f'Branch {branch_name_tgt_ui} based on {branch_name_src_ui} was created!',
                  category="success")
        else:
            branch_create_error = _branch_create_response_ui.get('error')
            flash(f'Branch create exception {branch_create_error}', category="danger")

        return redirect('/gh_branches_manager/')

    return abort(405)


@CONTROLLER_GH_UI.route('/gh_branches_manager/branch/<branch_name>/delete/',
                        methods=['GET', 'POST'])
def delete_branch(branch_name):
    """
    delete branch function
    :param branch_name:
    :return:
    """
    if request.method == "GET":
        return render_template('views/branch_deleter.html',
                               template_current_branch=branch_name)

    if request.method == "POST":
        _branch_delete_response_ui = common_functions.branch_deleter(branch_name=branch_name)
        branch_delete_status = _branch_delete_response_ui.get('status')

        if branch_delete_status == 200:
            flash(f'Branch {branch_name} was deleted!', category="success")
        else:
            branch_delete_error = _branch_delete_response_ui.get('error')
            flash('Branch delete exception {}'.format(branch_delete_error),
                  category="danger")

        return redirect('/gh_branches_manager/')

    return abort(405)


@CONTROLLER_GH_UI.route('/gh_files_manager/branch/<branch_name>/', methods=['GET'])
def gh_files_manager(branch_name):
    """
    github files manager function
    :param branch_name:
    :return:
    """
    _session_id_response_ui = common_functions.session_getter()
    gh_session_status, gh_session_id = _session_id_response_ui.get('status'), \
                                       _session_id_response_ui.get('content')
    flash(f'PyGithub connect success {gh_session_status}, {gh_session_id}', category="success")

    _branch_list_response_ui = common_functions.branch_lister()
    branch_list_status = _branch_list_response_ui.get('status')

    if branch_list_status == 200:
        branch_list_content = _branch_list_response_ui.get('content')
        flash(f'Branches load success {branch_list_status}', category="success")
    else:
        branch_list_error = _branch_list_response_ui.get('error')
        flash(f'Branches load exception {branch_list_error}', category="danger")
        return redirect('/')

    _files_list_response_ui = common_functions.file_lister(branch_name)
    files_list_status = _files_list_response_ui.get('status')

    if files_list_status == 200:
        files_list_content = _files_list_response_ui.get('content')
        flash(f'Files load success {files_list_status}', category="success")
    else:
        files_list_error = _files_list_response_ui.get('error')
        flash(f'Files load exception {files_list_error}', category="danger")
        return redirect('/')

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list_content,
                           template_current_branch=branch_name,
                           template_file_list=files_list_content)


@CONTROLLER_GH_UI.route('/gh_files_manager/branch/<branch_name>/file/create/',
                        methods=['GET', 'POST'])
def upload_file(branch_name):
    """
    upload file function
    :param branch_name:
    :return:
    """
    if request.method == "GET":
        return render_template('views/file_uploader.html',
                               template_current_branch=branch_name)

    if request.method == "POST":
        message = request.form['commit_message']

        try:
            file = request.files['uploaded_file']
            file_name, file_contents = utils.file_uploader_helper(file)

        # except FileNotFoundError in case file uploaded through textarea instead of input file
        except FileNotFoundError:
            file_contents = request.form['file_contents']
            file_name = request.form['file_name']

            if file_name == '':
                flash('No file uploaded, no file content found', category="danger")
                return redirect('/gh_files_manager/branch/' + branch_name)

        gh_file_path = GH_FILE_PATH_BASE + file_name

        _file_create_response_ui = common_functions.file_creator(
            gh_file_path=gh_file_path,
            message=message,
            content=file_contents,
            branch_name=branch_name)

        file_create_status = _file_create_response_ui.get('status')

        if file_create_status == 201:
            flash(f'File {file_name} was committed to the repository branch {branch_name} '
                  f'with the message {message}!', category="success")
        else:
            file_create_error = _file_create_response_ui.get('error')
            flash(f'File create exception {file_create_error}', category="danger")

        return redirect('/gh_files_manager/branch/' + branch_name)

    return abort(405)


@CONTROLLER_GH_UI.route('/gh_files_manager/branch/<branch_name>'
                        '/file/edit/<path:file_name>', methods=['GET', 'POST'])
def edit_file(branch_name, file_name):
    """
    edit file function
    :param branch_name:
    :param file_name:
    :return:
    """
    if request.method == "GET":
        _file_exists_response_ui = common_functions.file_exists_checker(gh_file_path=file_name,
                                                                        branch_name=branch_name)
        file_exists_status = _file_exists_response_ui.get('status')
        if file_exists_status == 200:

            # check if file is text-editable type to load up file contents for the form
            file_extension = os.path.splitext(str(file_name))[1]

            if file_extension in settings.EDITABLE_FILE_EXTENSION_LIST:
                file_contents = common_functions.file_content_getter(gh_file_path=file_name,
                                                                     branch_name=branch_name) \
                    .get('content')

                # if file is text-editable type but empty, the form shows the file content textarea
                if not file_contents:
                    file_contents = ''
            else:
                # file exists but is not text-editable type, the form shows the file upload
                file_contents = None

        else:
            file_exists_error = _file_exists_response_ui.get('error')
            flash(f'File exists exception {file_exists_error}', category="danger")
            return abort(404)

        return render_template('views/file_editor.html',
                               template_current_branch=branch_name,
                               file_name=file_name,
                               file_contents=file_contents)

    if request.method == "POST":
        message = request.form['commit_message']
        gh_file_path = file_name

        try:
            file = request.files['uploaded_file']

            if file:
                file_name_upload, file_contents = utils.file_uploader_helper(file)
                flash(f"File {file_name} is the target for contents from {file_name_upload}",
                      category="info")
            else:
                flash('No file uploaded', category="danger")
                return redirect('/gh_files_manager/branch/' + branch_name)

        # except FileNotFoundError in case file uploaded through textarea instead of input file
        # except BadRequestKeyError because the file_editor.html form objects are dynamically
        # generated so if no input file, your request.files['uploaded_file'] is a BadRequestKey
        except (FileNotFoundError, BadRequestKeyError):
            file_contents = request.form['file_contents']

        _file_edit_response_ui = common_functions.file_updater(
            gh_file_path=gh_file_path,
            message=message,
            content=file_contents,
            branch_name=branch_name)
        file_edit_status = _file_edit_response_ui.get('status')

        if file_edit_status == 200:
            flash(f'File {file_name} update was committed to the repository '
                  f'branch {branch_name} with the message {message}!',
                  category="success")
        elif file_edit_status != 200:
            file_edit_error = _file_edit_response_ui.get('error')
            flash(f'File edit exception {file_edit_error}', category="danger")

        return redirect('/gh_files_manager/branch/' + branch_name)

    return abort(405)


@CONTROLLER_GH_UI.route('/gh_files_manager/branch/<branch_name>'
                        '/file/delete/<path:file_name>', methods=['GET', 'POST'])
def delete_file(branch_name, file_name):
    """
    delete file function
    :param branch_name:
    :param file_name:
    :return:
    """
    if request.method == "GET":
        _file_exists_response_ui = common_functions.file_exists_checker(gh_file_path=file_name,
                                                                        branch_name=branch_name)
        file_exists_status = _file_exists_response_ui.get('status')

        if file_exists_status == 200:
            return render_template('views/file_deleter.html',
                                   template_current_branch=branch_name,
                                   file_name=file_name)

        file_exists_error = _file_exists_response_ui.get('error')
        flash(f'File exists exception {file_exists_error}', category="danger")
        return abort(404)

    if request.method == "POST":
        message = request.form['commit_message']
        _file_delete_response_ui = common_functions.file_deleter(
            gh_file_path=file_name,
            message=message,
            branch_name=branch_name)
        file_delete_status = _file_delete_response_ui.get('status')

        if file_delete_status == 200:
            flash(f'File {file_name} deletion was committed to the repository '
                  f'branch {branch_name} with the message {message}!', category="success")
        else:
            file_delete_error = _file_delete_response_ui.get('error')
            flash(f'File delete exception {file_delete_error}', category="danger")

        return redirect('/gh_files_manager/branch/' + branch_name)

    return abort(405)
