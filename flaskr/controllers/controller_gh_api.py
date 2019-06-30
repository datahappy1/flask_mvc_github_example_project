from flask import Blueprint, jsonify, request
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import utils


controller_gh_api = Blueprint('controller_gh_api', __name__)

# curl http://127.0.0.1:5000/api/gh_branches_manager/
@controller_gh_api.route('/api/gh_branches_manager/', methods=['GET'])
def gh_branches_manager():
    if request.method == "GET":
        gh_session_id = utils.session_getter()[0]
        branch_list = utils.branch_lister()
        response = jsonify({
            'gh_session_id': gh_session_id,
            'branches': branch_list,
            'repository': settings.repo
        })
        response.status_code = 200
        return response


#@controller_gh_api.route('/api/branch_creator/src/<branch_name_src>/tgt/<branch_name_tgt>', methods=['POST'])
@controller_gh_api.route('/api/branch/<branch_name>', methods=['POST','DELETE'])
def branch(branch_name):
    # if request.method == 'POST':
    #     branch_name = request.form['branch_name_tgt']
    #     branch_name_tgt = str(branch_name_tgt).replace(' ','')
    #     gh_session_id = utils.session_getter()[0]
    #     model_gh.Branch.create_branch(global_variables.obj,
    #                                   source_branch=branch_name_src,
    #                                   target_branch=branch_name_tgt)
    #     response = jsonify({
    #         'gh_session_id': gh_session_id,
    #         'repository': settings.repo,
    #         'branch_tgt': branch_name_tgt,
    #         'branch_src': branch_name_src
    #     })
    #     response.status_code = 201
    #     return response
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
        response.status_code = 204
        return response

# curl http://127.0.0.1:5000/api/gh_files_manager/branch/master/
@controller_gh_api.route('/api/gh_files_manager/branch/<branch_name>/', methods=['GET'])
def gh_files_manager(branch_name):
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


@controller_gh_api.route('/api/branch/<branch_name>/file/<file_name>/', methods=['GET','POST','PUT','DELETE'])
def file(branch_name, file_name):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass
