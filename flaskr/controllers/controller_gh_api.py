import os
from flask import Blueprint, jsonify, request
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import common_functions
from werkzeug.utils import secure_filename


controller_gh_api = Blueprint('controller_gh_api', __name__)


@controller_gh_api.route('/api/gh_branches_manager/', methods=['GET'])
def api_gh_branches_manager():
    if request.method == "GET":
        gh_session_id = common_functions.session_getter()[0]
        branch_list = common_functions.branch_lister()
        response = jsonify({
            'gh_session_id': gh_session_id,
            'branches': branch_list,
            'repository': settings.repo,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 200
        return response


@controller_gh_api.route('/api/branch/<branch_name>/', methods=['POST', 'DELETE'])
def api_branch(branch_name):
    if request.method == 'POST':
        args = request.args
        branch_name_src = args['branch_name_src']
        branch_name_tgt = branch_name
        branch_name_tgt = str(branch_name_tgt).replace(' ', '')
        gh_session_id = common_functions.session_getter()[0]
        model_gh.Branch.create_branch(global_variables.obj,
                                      source_branch=branch_name_src,
                                      target_branch=branch_name_tgt)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branch_tgt': branch_name_tgt,
            'branch_src': branch_name_src,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 201
        return response

    if request.method == 'DELETE':
        gh_session_id = common_functions.session_getter()[0]
        model_gh.Branch.delete_branch(global_variables.obj,
                                      branch_name=branch_name)

        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branch_name': branch_name,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 200
        return response


@controller_gh_api.route('/api/gh_files_manager/branch/<branch_name>/', methods=['GET'])
def api_gh_files_manager(branch_name):
    if request.method == "GET":
        gh_session_id = common_functions.session_getter()[0]
        branch_list = common_functions.branch_lister()
        files_list = common_functions.file_lister(branch_name)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'branches': branch_list,
            'repository': settings.repo,
            'current_branch': branch_name,
            'files': files_list,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 200
        return response


@controller_gh_api.route('/api/branch/<branch_name>/file/<file_name>/', methods=['POST', 'PUT', 'DELETE'])
def api_file(branch_name, file_name):
    if request.method == 'POST':
        args = request.args
        message = args['commit_message']
        gh_session_id = common_functions.session_getter()[0]
        file_name = secure_filename(file_name)
        file_contents = request.data
        #TODO remove file_contents start with b''
        model_gh.File.create_file(global_variables.obj,
                                  gh_file_path="flaskr/" + settings.repo_folder + file_name,
                                  message=message,
                                  content=file_contents,
                                  branch_name=branch_name)

        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'current_branch': branch_name,
            'file': file_name,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 201
        return response

    if request.method == 'PUT':
        args = request.args
        message = args['commit_message']
        gh_session_id = common_functions.session_getter()[0]
        file_name = secure_filename(file_name)
        file_contents = request.data
        #TODO remove file_contents start with b''
        model_gh.File.update_file(global_variables.obj,
                                  gh_file_path="flaskr/" + settings.repo_folder + file_name,
                                  message=message,
                                  content=file_contents,
                                  branch_name=branch_name)

        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'current_branch': branch_name,
            'file': file_name,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 201
        return response

    if request.method == 'DELETE':
        args = request.args
        message = args['commit_message']
        gh_session_id = common_functions.session_getter()[0]
        model_gh.File.delete_file(global_variables.obj,
                                  gh_file_path="flaskr/" + settings.repo_folder + file_name,
                                  message=message,
                                  branch_name=branch_name)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'current_branch': branch_name,
            'file': file_name,
            'method': request.method,
            'status': 'OK',
            'mimetype': 'application/json'
        })
        response.status_code = 200
        return response
