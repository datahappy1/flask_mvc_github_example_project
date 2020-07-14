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
    return model_gh.GhBaseModel.get_session_id(model_gh.GlobalGhModel)


def branch_lister() -> dict:
    """
    branch lister function
    :return:
    """
    return model_gh.GhBranch.list_all_branches(model_gh.GlobalGhModel)


def branch_creator(source_branch_name, target_branch_name):
    """
    branch creator function
    :param source_branch_name:
    :param target_branch_name:
    :return:
    """
    return model_gh.GhBranch.create_branch(model_gh.GlobalGhModel,
                                           source_branch=source_branch_name,
                                           target_branch=target_branch_name)


def branch_deleter(branch_name):
    """
    branch deleter function
    :param branch_name:
    :return:
    """
    return model_gh.GhBranch.delete_branch(model_gh.GlobalGhModel,
                                           branch_name=branch_name)


def file_lister(branch_name) -> dict:
    """
    file lister function
    :param branch_name:
    :return:
    """
    files_list = model_gh.GhFile.list_all_files(model_gh.GlobalGhModel, branch_name)
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
    return model_gh.GhFile.get_file_status(model_gh.GlobalGhModel,
                                           gh_file_path, branch_name)


def file_content_getter(gh_file_path, branch_name) -> dict:
    """
    file content getter function
    :param gh_file_path:
    :param branch_name:
    :return:
    """
    return model_gh.GhFile.get_file_contents(model_gh.GlobalGhModel,
                                             gh_file_path, branch_name)


def file_creator(gh_file_path, message, content, branch_name):
    """
    file creator function
    :param gh_file_path:
    :param message:
    :param content:
    :param branch_name:
    :return:
    """
    return model_gh.GhFile.create_file(model_gh.GlobalGhModel,
                                       gh_file_path=gh_file_path,
                                       message=message,
                                       content=content,
                                       branch_name=branch_name)


def file_updater(gh_file_path, message, content, branch_name):
    """
    file updater function
    :param gh_file_path:
    :param message:
    :param content:
    :param branch_name:
    :return:
    """
    return model_gh.GhFile.update_file(model_gh.GlobalGhModel,
                                       gh_file_path=gh_file_path,
                                       message=message,
                                       content=content,
                                       branch_name=branch_name)


def file_deleter(gh_file_path, message, branch_name):
    """
    file deleter function
    :param gh_file_path:
    :param message:
    :param branch_name:
    :return:
    """
    return model_gh.GhFile.delete_file(model_gh.GlobalGhModel,
                                       gh_file_path=gh_file_path,
                                       message=message,
                                       branch_name=branch_name)
