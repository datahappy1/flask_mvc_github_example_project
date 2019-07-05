"""
common functions module
"""
import os

from flaskr.lib import global_variables, settings
from flaskr.models import model_gh


# controller functions
def session_getter() -> dict:
    """
    session getter function
    :return:
    """
    github_session_id = model_gh.Model.get_session_id(global_variables.OBJ)
    return github_session_id


def branch_lister() -> dict:
    """
    branch lister function
    :return:
    """
    branch_list = model_gh.Branch.list_all_branches(global_variables.OBJ)
    return branch_list


def file_lister(branch_name) -> dict:
    """
    file lister function
    :param branch_name:
    :return:
    """
    files_list = model_gh.File.list_all_files(global_variables.OBJ, branch_name)
    if files_list.get('status') == 200:
        _files_list = []
        for file in files_list.get('content'):
            file_extension = os.path.splitext(str(file))[1]
            if file_extension in settings.EDITABLE_FILE_EXTENSION_LIST:
                _files_list.append([file, True])
            else:
                _files_list.append([file, False])
        files_list['content'] = _files_list
    return files_list


def file_exists_checker(gh_file_path, branch_name) -> dict:
    """
    file exists checker function
    :param gh_file_path:
    :param branch_name:
    :return:
    """
    github_file_status = model_gh.File.get_file_status(global_variables.OBJ,
                                                       gh_file_path, branch_name)
    return github_file_status


def file_content_getter(gh_file_path, branch_name) -> dict:
    """
    file content getter function
    :param gh_file_path:
    :param branch_name:
    :return:
    """
    github_file_content = model_gh.File.get_file_contents(global_variables.OBJ,
                                                          gh_file_path, branch_name)
    return github_file_content
