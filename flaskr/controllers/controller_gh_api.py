import os
from flask import Blueprint, jsonify, request
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import utils
from werkzeug.utils import secure_filename


controller_gh_api = Blueprint('controller_gh_api', __name__)


# curl http://127.0.0.1:5000/api/gh_branches_manager/
@controller_gh_api.route('/api/gh_branches_manager/', methods=['GET'])
def api_gh_branches_manager():
    if request.method == "GET":
        gh_session_id = utils.session_getter()[0]
        branch_list = utils.branch_lister()
        response = jsonify({
            'gh_session_id': gh_session_id,
            'branches': branch_list,
            'repository': settings.repo,
            'status': 'OK', #httplib.OK,
            'mimetype': 'application/json'
        })
        response.status_code = 200
        return response


# curl -X POST http://127.0.0.1:5000/api/branch/test2?branch_name_src=test
# curl -X DELETE http://127.0.0.1:5000/api/branch/test/
@controller_gh_api.route('/api/branch/<branch_name>', methods=['POST', 'DELETE'])
def api_branch(branch_name):
    if request.method == 'POST':
        args = request.args
        branch_name_src = args['branch_name_src']
        branch_name_tgt = branch_name
        branch_name_tgt = str(branch_name_tgt).replace(' ', '')
        gh_session_id = utils.session_getter()[0]
        model_gh.Branch.create_branch(global_variables.obj,
                                      source_branch=branch_name_src,
                                      target_branch=branch_name_tgt)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branch_tgt': branch_name_tgt,
            'branch_src': branch_name_src,
            'method': request.method
        })
        response.status_code = 201
        return response

    if request.method == 'DELETE':
        gh_session_id = utils.session_getter()[0]
        model_gh.Branch.delete_branch(global_variables.obj,
                                      branch_name=branch_name)

        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branch_name': branch_name,
            'method': request.method
        })
        response.status_code = 200
        return response


# curl http://127.0.0.1:5000/api/gh_files_manager/branch/master/
@controller_gh_api.route('/api/gh_files_manager/branch/<branch_name>/', methods=['GET'])
def api_gh_files_manager(branch_name):
    if request.method == "GET":
        gh_session_id = utils.session_getter()[0]
        branch_list = utils.branch_lister()
        files_list = utils.file_lister(branch_name)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'branches': branch_list,
            'repository': settings.repo,
            'current_branch': branch_name,
            'files': files_list
        })
        response.status_code = 200
        return response


# curl -d "data=@path/to/my-file.txt" POST http://127.0.0.1:5000/api/branch/master/my-file.txt?commit_message="curl commit"
# curl -d "data=@path/to/my-file.txt" PUT http://127.0.0.1:5000/api/branch/master/my-file.txt?commit_message="curl commit"
# curl -d "data=@path/to/my-file.txt" DELETE http://127.0.0.1:5000/api/branch/master/my-file.txt?commit_message="curl commit"
@controller_gh_api.route('/api/branch/<branch_name>/file/<file_name>/', methods=['POST', 'PUT', 'DELETE'])
def api_file(branch_name, file_name):
    if request.method == 'POST':
        args = request.args
        message = args['commit_message']
        gh_session_id = utils.session_getter()[0]
        file_name = secure_filename(file_name.filename)

        temp_file_path = os.path.join(os.getcwd(), 'temp', file_name)
        with open(temp_file_path, "wb") as temp_file_handler:
            file_contents = temp_file_handler.read(request.data)

        model_gh.File.create_file(global_variables.obj,
                                  gh_file_path="flaskr/" + settings.repo_folder + file_name,
                                  message=message,
                                  content=file_contents,
                                  branch_name=branch_name)

        os.unlink(temp_file_path)
        assert not os.path.exists(temp_file_path)

        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'current_branch': branch_name,
            'file': file_name,
            'method': request.method
        })
        response.status_code = 201
        return response

    if request.method == 'PUT':
        args = request.args
        message = args['commit_message']
        gh_session_id = utils.session_getter()[0]

        temp_file_path = os.path.join(os.getcwd(), 'temp', file_name)
        with open(temp_file_path, "wb") as temp_file_handler:
            file_contents = temp_file_handler.read(request.data)

        model_gh.File.update_file(global_variables.obj,
                                  gh_file_path=file_name,
                                  message=message,
                                  content=file_contents,
                                  branch_name=branch_name)

        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'current_branch': branch_name,
            'file': file_name,
            'method': request.method
        })
        response.status_code = 201
        return response

    if request.method == 'DELETE':
        args = request.args
        message = args['commit_message']
        gh_session_id = utils.session_getter()[0]
        model_gh.File.delete_file(global_variables.obj,
                                  gh_file_path=file_name,
                                  message=message,
                                  branch_name=branch_name)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'current_branch': branch_name,
            'file': file_name,
            'method': request.method
        })
        response.status_code = 200
        return response