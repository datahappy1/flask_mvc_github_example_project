"""
controller github api module
"""
import os

from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest, NotFound
from flask import Blueprint, jsonify, request

from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import common_functions


CONTROLLER_GH_API = Blueprint('controller_gh_api', __name__)


def custom_error(status_code):
    """
    custom error handling function
    :param status_code:
    :return:
    """
    if status_code == 404:
        custom_error_response = jsonify(404, "resource not found")
    elif status_code == 405:
        custom_error_response = jsonify(405, "method not allowed")
    else:
        custom_error_response = jsonify(400, "bad request")
    return custom_error_response


@CONTROLLER_GH_API.route('/api/version1/resource/branches/all/', methods=['GET'])
def api_gh_branches_manager():
    """
    api github branches manager endpoint function
    :return:
    """
    if request.method == "GET":
        _branch_list = common_functions.branch_lister()
        branch_list_status = _branch_list.get('status')

        if branch_list_status == 200:
            branch_list_content = _branch_list.get('content')
            response = jsonify({
                'branches': branch_list_content,
                'repository': settings.REPO,
                'method': request.method,
                'status': branch_list_status,
                'mimetype': 'application/json'
            })
        else:
            branch_list_error = _branch_list.get('error')
            response = jsonify({
                'status': branch_list_status,
                'errors': branch_list_error,
                'mimetype': 'application/json'
            })
        response.status_code = branch_list_status
        return response
    else:
        custom_error(405)


@CONTROLLER_GH_API.route('/api/version1/resource/branch/', methods=['POST'])
def api_create_branch():
    """
    api create branch endpoint function
    :param branch_name:
    :return:
    """
    if request.method == 'POST':
        branch_name_src = request.form['branch_name_src']
        branch_name_tgt = request.form['branch_name_tgt']
        _branch_create = model_gh.Branch.create_branch(global_variables.OBJ,
                                                       source_branch=branch_name_src,
                                                       target_branch=branch_name_tgt)
        branch_create_status = _branch_create.get('status')

        if branch_create_status == 201:
            response = jsonify({
                'repository': settings.REPO,
                'branch_target': branch_name_tgt,
                'branch_source': branch_name_src,
                'method': request.method,
                'status': branch_create_status,
                'mimetype': 'application/json'
            })
        else:
            branch_create_error = _branch_create.get('error')
            response = jsonify({
                'status': branch_create_status,
                'errors': branch_create_error,
                'mimetype': 'application/json'
            })
        response.status_code = branch_create_status
        return response
    else:
        custom_error(405)


@CONTROLLER_GH_API.route('/api/version1/resource/branch/<branch_name>/', methods=['DELETE'])
def api_existing_branch(branch_name):
    """
    api existing branch endpoint function
    :param branch_name:
    :return:
    """
    if request.method == 'DELETE':
        _branch_delete = model_gh.Branch.delete_branch(global_variables.OBJ,
                                                       branch_name=branch_name)
        branch_delete_status = _branch_delete.get('status')

        if branch_delete_status == 200:
            response = jsonify({
                'repository': settings.REPO,
                'branch_name': branch_name,
                'method': request.method,
                'status': branch_delete_status,
                'mimetype': 'application/json'
            })
        else:
            branch_delete_error = _branch_delete.get('error')
            response = jsonify({
                'status': branch_delete_status,
                'errors': branch_delete_error,
                'mimetype': 'application/json'
            })
        response.status_code = branch_delete_status
        return response
    else:
        custom_error(405)


@CONTROLLER_GH_API.route('/api/version1/resource/branch/<branch_name>/files/all/', methods=['GET'])
def api_gh_files_manager(branch_name):
    """
    api github files manager endpoint function
    :param branch_name:
    :return:
    """
    if request.method == "GET":
        _branch_list = common_functions.branch_lister()
        branch_list_status = _branch_list.get('status')
        _files_list = common_functions.file_lister(branch_name)
        files_list_status = _files_list.get('status')

        if branch_list_status == 200 and files_list_status == 200:
            branch_list_content = _branch_list.get('content')
            files_list_content = _files_list.get('content')
            response = jsonify({
                'branches': branch_list_content,
                'repository': settings.REPO,
                'current_branch': branch_name,
                'files': files_list_content,
                'method': request.method,
                'status': 'OK',
                'mimetype': 'application/json'
            })
        else:
            branch_list_error = _branch_list.get('error')
            files_list_error = _files_list.get('error')
            response = jsonify({
                'status': files_list_status,
                'errors': [branch_list_error, files_list_error],
                'mimetype': 'application/json'
            })
        response.status_code = files_list_status
        return response
    else:
        custom_error(405)


@CONTROLLER_GH_API.route('/api/version1/resource/branch/<branch_name>/file/', methods=['POST'])
def api_create_file(branch_name):
    """
    api create file endpoint function

    curl post files example:
    curl - X POST - F commit_message=Test - F uploaded_file=@/home/filepathxxx http://127.0.0.1:5000/api/branch/dev/file/filenamexxx/

    :param branch_name:
    :param file_name:
    :return:
    """
    if request.method == 'POST':
        message = request.form['commit_message']

        try:
            file = request.files['uploaded_file']
            file_name = secure_filename(file.filename)
            temp_file_path = os.path.join(os.getcwd(), 'temp', file_name)
            file.save(temp_file_path)

            with open(temp_file_path, 'rb') as temp_file_handler:
                file_contents = temp_file_handler.read()

            os.unlink(temp_file_path)
            assert not os.path.exists(temp_file_path)

        except BadRequest:
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
            response = jsonify({
                'repository': settings.REPO,
                'current_branch': branch_name,
                'file': file_name,
                'method': request.method,
                'status': file_create_status,
                'mimetype': 'application/json'
            })
        else:
            file_create_error = _file_create.get('error')
            response = jsonify({
                'status': file_create_status,
                'errors': file_create_error,
                'mimetype': 'application/json'
            })
        response.status_code = file_create_status
        return response
    else:
        custom_error(405)


@CONTROLLER_GH_API.route('/api/version1/resource/branch/<branch_name>/file/<file_name>/', methods=['PUT', 'DELETE'])
def api_existing_file(branch_name, file_name):
    """
    api existing file endpoint function
    :param branch_name:
    :param file_name:
    :return:
    """
    message = request.form['commit_message']
    file_name = secure_filename(file_name)
    gh_file_path = "flaskr/" + settings.REPO_FOLDER + file_name

    if request.method == 'PUT':
        try:
            file_contents = request.form['file_contents']

        except BadRequest:
            # file_contents not coming from the edit textarea form means file
            # is not editable extension type therefore get the file uploaded with the form
            file = request.files['uploaded_file']
            temp_file_path = os.path.join(os.getcwd(), 'temp', file_name)
            file.save(temp_file_path)

            with open(temp_file_path, 'rb') as temp_file_handler:
                file_contents = temp_file_handler.read()

            gh_file_path = "flaskr/" + settings.REPO_FOLDER + file_name

            os.unlink(temp_file_path)
            assert not os.path.exists(temp_file_path)

        _file_update = model_gh.File.update_file(global_variables.OBJ,
                                                 gh_file_path=gh_file_path,
                                                 message=message,
                                                 content=file_contents,
                                                 branch_name=branch_name)

        file_update_status = _file_update.get('status')

        if file_update_status == 201:
            response = jsonify({
                'repository': settings.REPO,
                'current_branch': branch_name,
                'file': file_name,
                'method': request.method,
                'status': file_update_status,
                'mimetype': 'application/json'
            })
        else:
            file_update_error = _file_update.get('error')
            response = jsonify({
                'status': file_update_status,
                'errors': file_update_error,
                'mimetype': 'application/json'
            })
        response.status_code = file_update_status
        return response

    if request.method == 'DELETE':
        _file_delete = model_gh.File.delete_file(global_variables.OBJ,
                                                 gh_file_path=gh_file_path,
                                                 message=message,
                                                 branch_name=branch_name)

        file_delete_status = _file_delete.get('status')

        if file_delete_status == 201:
            response = jsonify({
                'repository': settings.REPO,
                'current_branch': branch_name,
                'file': file_name,
                'method': request.method,
                'status': file_delete_status,
                'mimetype': 'application/json'
            })
        else:
            file_update_error = _file_delete.get('error')
            response = jsonify({
                'status': file_delete_status,
                'errors': file_update_error,
                'mimetype': 'application/json'
            })
        response.status_code = file_delete_status
        return response
    else:
        custom_error(405)
