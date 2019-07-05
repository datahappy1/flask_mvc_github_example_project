"""
controller github api module
"""
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request

from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import common_functions


CONTROLLER_GH_API = Blueprint('controller_gh_api', __name__)


@CONTROLLER_GH_API.route('/api/gh_branches_manager/',
                         methods=['GET'])
def api_gh_branches_manager():
    """
    api github branches manager endpoint function
    :return:
    """
    if request.method == "GET":
        _session_id = common_functions.session_getter()
        session_id_status = _session_id.get('status')

        if session_id_status == 200:
            _branch_list = common_functions.branch_lister()
            branch_list_status = _branch_list.get('status')

            if branch_list_status == 200:
                session_id_content = str(_session_id.get('content'))
                branch_list_content = _branch_list.get('content')
                response = jsonify({
                    'session_id': session_id_content,
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
        else:
            session_id_error = _session_id.get('errors')
            response = jsonify({
                'status': session_id_status,
                'errors:': session_id_error,
                'mimetype': 'application/json'
            })
        response.status_code = session_id_status
        return response


@CONTROLLER_GH_API.route('/api/branch/<branch_name>/',
                         methods=['POST', 'DELETE'])
def api_branch(branch_name):
    """
    api branch endpoint function
    :param branch_name:
    :return:
    """
    if request.method == 'POST':
        args = request.args
        branch_name_src = args['branch_name_src']
        branch_name_tgt = branch_name
        branch_name_tgt = str(branch_name_tgt).replace(' ', '')
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


@CONTROLLER_GH_API.route('/api/gh_files_manager/branch/<branch_name>/',
                         methods=['GET'])
def api_gh_files_manager(branch_name):
    """
    api github files manager endpoint function
    :param branch_name:
    :return:
    """
    if request.method == "GET":
        _session_id = common_functions.session_getter()
        session_id_status = _session_id.get('status')

        if session_id_status == 200:
            _branch_list = common_functions.branch_lister()
            branch_list_status = _branch_list.get('status')
            _files_list = common_functions.file_lister(branch_name)
            files_list_status = _files_list.get('status')

            if branch_list_status == 200 and files_list_status == 200:
                session_id_content = str(_session_id.get('content'))
                branch_list_content = _branch_list.get('content')
                files_list_content = _files_list.get('content')
                response = jsonify({
                    'gh_session_id': session_id_content,
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

        else:
            session_id_error = _session_id.get('errors')
            response = jsonify({
                'status': session_id_status,
                'errors:': session_id_error,
                'mimetype': 'application/json'
            })
            response.status_code = session_id_status

        return response


@CONTROLLER_GH_API.route('/api/branch/<branch_name>/file/<file_name>/',
                         methods=['POST', 'PUT', 'DELETE'])
def api_file(branch_name, file_name):
    """
    api file endpoint function
    :param branch_name:
    :param file_name:
    :return:
    """
    if request.method == 'POST':
        args = request.args
        message = args['commit_message']
        file_name = secure_filename(file_name)
        file_contents = request.data
        _file_create = model_gh.File.create_file(global_variables.OBJ,
                                                 gh_file_path="flaskr/"
                                                 + settings.REPO_FOLDER
                                                 + file_name,
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

    if request.method == 'PUT':
        args = request.args
        message = args['commit_message']
        file_name = secure_filename(file_name)
        file_contents = request.data
        _file_update = model_gh.File.update_file(global_variables.OBJ,
                                                 gh_file_path="flaskr/"
                                                 + settings.REPO_FOLDER
                                                 + file_name,
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
        args = request.args
        message = args['commit_message']
        _file_delete = model_gh.File.delete_file(global_variables.OBJ,
                                                 gh_file_path="flaskr/"
                                                 + settings.REPO_FOLDER
                                                 + file_name,
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
