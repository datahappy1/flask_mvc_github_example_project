from flask import Blueprint, jsonify, request
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from flaskr.controllers import utils


controller_gh_api = Blueprint('controller_gh_api', __name__)


@controller_gh_api.route('/api/gh_branches_manager/')
def gh_branches_manager():
    if request.method == "GET":
        gh_session_id = utils.session_getter()[0]
        branch_list = utils.branch_lister()
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branches': branch_list
        })
        response.status_code = 200
        return response


@controller_gh_api.route('/api/branch_creator/src/<branch_name_src>/tgt/<branch_name_tgt>', methods=['POST'])
def create_branch(branch_name_src, branch_name_tgt):
    if request.method == 'POST':
        branch_name_tgt = request.form['branch_name_tgt']
        branch_name_tgt = str(branch_name_tgt).replace(' ','')
        gh_session_id = utils.session_getter()[0]
        model_gh.Branch.create_branch(global_variables.obj,
                                      source_branch=branch_name_src,
                                      target_branch=branch_name_tgt)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branch_tgt': branch_name_tgt,
            'branch_src': branch_name_src
        })
        response.status_code = 201
        return response


@controller_gh_api.route('/api/branch/<branch_name>', methods=['POST'])
def delete_branch(branch_name):
    if request.method == 'POST':
        branch_name_tgt = request.form['branch_name_tgt']
        branch_name_tgt = str(branch_name_tgt).replace(' ','')
        gh_session_id = utils.session_getter()[0]
        model_gh.Branch.create_branch(global_variables.obj,
                                      source_branch=branch_name_src,
                                      target_branch=branch_name_tgt)
        response = jsonify({
            'gh_session_id': gh_session_id,
            'repository': settings.repo,
            'branch_tgt': branch_name_tgt,
            'branch_src': branch_name_src
        })
        response.status_code = 201
        return response