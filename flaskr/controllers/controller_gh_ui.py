"""
controller github ui module
"""
import os

from flask import Blueprint, request, flash, redirect, render_template, abort

from flaskr.project_variables import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import common_functions

CONTROLLER_GH_UI = Blueprint('controller_gh_ui', __name__,
                             template_folder='templates')


# @controller_gh.routes - views functions for ui user interaction
# optionally validating the inputs and returning redirects or rendering templates
# with the html forms
@CONTROLLER_GH_UI.route('/views/gh_branches_manager/', methods=['GET'])
def gh_branches_manager():
    """
    github branches manager function
    :return:
    """
    _session_id = common_functions.session_getter()
    gh_session_status, gh_session_id = _session_id.get('status'), _session_id.get('content')
    flash(f'PyGithub connect success {gh_session_status}, {gh_session_id}', category="success")

    _branch_list = common_functions.branch_lister()
    branch_list_status = _branch_list.get('status')
    if branch_list_status == 200:
        branch_list_content = _branch_list.get('content')
        flash(f'Branches load success {branch_list_status}', category="success")
    else:
        branch_list_error = _branch_list.get('error')
        flash(f'Branches load exception {branch_list_error}', category="warning")
        return redirect('/')

    return render_template('views/gh_branches_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list_content,
                           template_repo_name=settings.REPO)


@CONTROLLER_GH_UI.route('/views/gh_branches_manager/branch/<branch_name>/create/', methods=['GET'])
def create_branch(branch_name):
    """
    create branch function
    :param branch_name:
    :return:
    """
    return render_template('views/branch_creator.html',
                           template_current_branch=branch_name)


@CONTROLLER_GH_UI.route('/views/gh_branches_manager/branch/<branch_name>/delete/', methods=['GET'])
def delete_branch(branch_name):
    """
    delete branch function
    :param branch_name:
    :return:
    """
    return render_template('views/branch_deleter.html',
                           template_current_branch=branch_name)


@CONTROLLER_GH_UI.route('/views/gh_files_manager/branch/<branch_name>/', methods=['GET'])
def gh_files_manager(branch_name):
    """
    github files manager function
    :param branch_name:
    :return:
    """
    _session_id = common_functions.session_getter()
    gh_session_status, gh_session_id = _session_id.get('status'), _session_id.get('content')
    flash(f'PyGithub connect success {gh_session_status}, {gh_session_id}', category="success")

    _branch_list = common_functions.branch_lister()
    branch_list_status = _branch_list.get('status')
    if branch_list_status == 200:
        branch_list_content = _branch_list.get('content')
        flash(f'Branches load success {branch_list_status}', category="success")
    else:
        branch_list_error = _branch_list.get('error')
        flash(f'Branches load exception {branch_list_error}', category="warning")
        return redirect('/')

    _files_list = common_functions.file_lister(branch_name)
    files_list_status = _files_list.get('status')
    if files_list_status == 200:
        files_list_content = _files_list.get('content')
        flash(f'Files load success {files_list_status}', category="success")
    else:
        files_list_error = _files_list.get('error')
        flash(f'Files load exception {files_list_error}', category="warning")
        return redirect('/')

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list_content,
                           template_current_branch=branch_name,
                           template_file_list=files_list_content)


@CONTROLLER_GH_UI.route('/views/gh_files_manager/branch/<branch_name>/file/create/',
                        methods=['GET'])
def upload_file(branch_name):
    """
    upload file function
    :param branch_name:
    :return:
    """
    return render_template('views/file_uploader.html',
                           template_current_branch=branch_name)


@CONTROLLER_GH_UI.route('/views/gh_files_manager/branch/<branch_name>/file/edit/<path:file_name>',
                        methods=['GET'])
def edit_file(branch_name, file_name):
    """
    edit file function
    :param branch_name:
    :param file_name:
    :return:
    """
    _file_exists = common_functions.file_exists_checker(gh_file_path=file_name,
                                                        branch_name=branch_name)
    file_exists_status = _file_exists.get('status')
    if file_exists_status == 200:

        # check if file is editable to load up file contents for the form
        file_extension = os.path.splitext(str(file_name))[1]
        if file_extension in settings.EDITABLE_FILE_EXTENSION_LIST:
            file_contents = common_functions.file_content_getter(gh_file_path=file_name,
                                                                 branch_name=branch_name)\
                .get('content')
        else:
            # file exists but is not editable
            file_contents = None

        return render_template('views/file_editor.html',
                               template_current_branch=branch_name,
                               file_name=file_name,
                               file_contents=file_contents)
    else:
        file_exists_error = _file_exists.get('error')
        flash(f'File exists exception {file_exists_error}', category="warning")

        return redirect('/views/gh_files_manager/branch/' + branch_name)


@CONTROLLER_GH_UI.route('/views/gh_files_manager/branch/<branch_name>'
                        '/file/delete/<path:file_name>', methods=['GET'])
def delete_file(branch_name, file_name):
    """
    delete file function
    :param branch_name:
    :param file_name:
    :return:
    """
    _file_exists = common_functions.file_exists_checker(gh_file_path=file_name,
                                                        branch_name=branch_name)
    file_exists_status = _file_exists.get('status')
    if file_exists_status == 200:
        return render_template('views/file_deleter.html',
                               template_current_branch=branch_name,
                               file_name=file_name)

    file_exists_error = _file_exists.get('error')
    flash(f'File exists exception {file_exists_error}', category="warning")

    return redirect('/views/gh_files_manager/branch/' + branch_name)


# @controller_gh.routes - worker functions accepting form requests from the html forms,
# proceeding with the desired actions and returning redirects to lead the
# ui user back to the branches or files manager
@CONTROLLER_GH_UI.route('/branch_creator/', methods=['GET', 'POST'])
def branch_creator():
    """
    branch creator function
    :return:
    """
    if request.method == 'POST':
        branch_name_src_ui = request.form['branch_name_src']
        branch_name_tgt_ui = request.form['branch_name_tgt']
        _branch_create = model_gh.Branch.create_branch(global_variables.OBJ,
                                                       source_branch=branch_name_src_ui,
                                                       target_branch=branch_name_tgt_ui)
        branch_create_status = _branch_create.get('status')
        if branch_create_status == 201:
            flash(f'Branch {branch_name_tgt_ui} based on {branch_name_src_ui} was created!',
                  category="success")
        elif branch_create_status != 201:
            branch_create_error = _branch_create.get('error')
            flash(f'Branch create exception {branch_create_error}', category="warning")

        return redirect('/views/gh_branches_manager/')
    else:
        return abort(405)


@CONTROLLER_GH_UI.route('/branch_deleter/<branch_name>/', methods=['GET', 'POST'])
def branch_deleter(branch_name):
    """
    branch deleter function
    :param branch_name:
    :return:
    """
    if request.method == 'POST':
        _branch_delete = model_gh.Branch.delete_branch(global_variables.OBJ,
                                                       branch_name=branch_name)
        branch_delete_status = _branch_delete.get('status')
        if branch_delete_status == 200:
            flash(f'Branch {branch_name} was deleted!', category="success")
        elif branch_delete_status != 200:
            branch_delete_error = _branch_delete.get('error')
            flash('Branch delete exception {}'.format(branch_delete_error),
                  category="warning")

        return redirect('/views/gh_branches_manager/')
    else:
        return abort(405)


@CONTROLLER_GH_UI.route('/file_uploader/<branch_name>/', methods=['GET', 'POST'])
def file_uploader(branch_name):
    """
    file uploader function
    :param branch_name:
    :return:
    """
    if request.method == 'POST':
        message = request.form['commit_message']

        try:
            file = request.files['uploaded_file']
            file_name, file_contents = common_functions.file_uploader_helper(file)

        except FileNotFoundError:
            file_contents = request.form['file_contents']
            file_name = request.form['file_name']

        gh_file_path = "flaskr/" + settings.REPO_FOLDER + file_name

        _file_create = model_gh.File.create_file(global_variables.OBJ,
                                                 gh_file_path=gh_file_path,
                                                 message=message,
                                                 content=file_contents,
                                                 branch_name=branch_name)

        file_create_status = _file_create.get('status')

        if file_create_status == 201:
            flash(f'File {file_name} was committed to the repository branch {branch_name} '
                  f'with the message {message}!', category="success")
        elif file_create_status != 201:
            file_create_error = _file_create.get('error')
            flash(f'File create exception {file_create_error}', category="warning")

        return redirect('/views/gh_files_manager/branch/' + branch_name)
    else:
        return abort(405)


@CONTROLLER_GH_UI.route('/file_editor/<branch_name>/file/edit/<path:file_name>',
                        methods=['GET', 'POST'])
def file_editor(branch_name, file_name):
    """
    file editor function
    :param branch_name:
    :param file_name:
    :return:
    """
    if request.method == 'POST':
        message = request.form['commit_message']
        try:
            file_contents = request.form['file_contents']
            gh_file_path = file_name

        except FileNotFoundError:
            # file_contents not coming from the edit textarea form means file
            # is not editable extension type therefore get the file uploaded with the form
            file = request.files['uploaded_file']
            file_name, file_contents = common_functions.file_uploader_helper(file)

            gh_file_path = "flaskr/" + settings.REPO_FOLDER + file_name

        _file_edit = model_gh.File.update_file(global_variables.OBJ,
                                               gh_file_path=gh_file_path,
                                               message=message,
                                               content=file_contents,
                                               branch_name=branch_name)
        file_edit_status = _file_edit.get('status')
        if file_edit_status == 201:
            flash(f'File {file_name} update was committed to the repository '
                  f'branch {branch_name} with the message {message}!', category="success")
        elif file_edit_status != 201:
            file_edit_error = _file_edit.get('error')
            flash(f'File edit exception {file_edit_error}', category="warning")

        return redirect('/views/gh_files_manager/branch/' + branch_name)
    else:
        return abort(405)


@CONTROLLER_GH_UI.route('/file_deleter/<branch_name>/file/delete/'
                        '<path:file_name>', methods=['GET', 'POST'])
def file_deleter(branch_name, file_name):
    """
    file deleter function
    :param branch_name:
    :param file_name:
    :return:
    """
    if request.method == 'POST':
        message = request.form['commit_message']
        _file_delete = model_gh.File.delete_file(global_variables.OBJ,
                                                 gh_file_path=file_name,
                                                 message=message,
                                                 branch_name=branch_name)
        file_delete_status = _file_delete.get('status')
        if file_delete_status == 200:
            flash(f'File {file_name} deletion was committed to the repository '
                  f'branch {branch_name} with the message {message}!', category="success")
        elif file_delete_status != 201:
            file_delete_error = _file_delete.get('error')
            flash(f'File delete exception {file_delete_error}', category="warning")

        return redirect('/views/gh_files_manager/branch/' + branch_name)
    else:
        return abort(405)
