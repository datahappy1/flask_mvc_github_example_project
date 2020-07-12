"""
common functions module
"""
import os

from flaskr import settings
from flaskr.models import model_gh


# controller functions
def session_getter() -> dict:
    """
    session getter function
    :return:
    """

    github_session_id = model_gh.Model.get_session_id(model_gh.Global)
    return github_session_id


def branch_lister() -> dict:
    """
    branch lister function
    :return:
    """
    branch_list = model_gh.Branch.list_all_branches(model_gh.Global)
    return branch_list


def branch_creator(source_branch_name, target_branch_name):
    return model_gh.Branch.create_branch(model_gh.Global,
                                         source_branch=source_branch_name,
                                         target_branch=target_branch_name)


def branch_deleter(branch_name):
    return model_gh.Branch.delete_branch(model_gh.Global,
                                         branch_name=branch_name)


def file_lister(branch_name) -> dict:
    """
    file lister function
    :param branch_name:
    :return:
    """
    files_list = model_gh.File.list_all_files(model_gh.Global, branch_name)
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
    return model_gh.File.get_file_status(model_gh.Global,
                                         gh_file_path, branch_name)


def file_content_getter(gh_file_path, branch_name) -> dict:
    """
    file content getter function
    :param gh_file_path:
    :param branch_name:
    :return:
    """
    return model_gh.File.get_file_contents(model_gh.Global,
                                           gh_file_path, branch_name)


def file_creator(gh_file_path, message, content, branch_name):
    return model_gh.File.create_file(model_gh.Global,
                                     gh_file_path=gh_file_path,
                                     message=message,
                                     content=content,
                                     branch_name=branch_name)


def file_updater(gh_file_path, message, content, branch_name):
    return model_gh.File.update_file(model_gh.Global,
                                     gh_file_path=gh_file_path,
                                     message=message,
                                     content=content,
                                     branch_name=branch_name)


def file_deleter(gh_file_path, message, branch_name):
    return model_gh.File.delete_file(model_gh.Global,
                                     gh_file_path=gh_file_path,
                                     message=message,
                                     branch_name=branch_name)
