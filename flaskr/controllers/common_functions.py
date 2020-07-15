"""
common functions module
"""
import os

from flaskr import settings
from flaskr.models.model_global import MODEL_GLOBAL_DICT
from flaskr.models.model_gh import GhBaseModel, GhBranch, GhFile


# controller functions
def session_getter() -> dict:
    """
    session getter function
    :return:
    """
    return GhBaseModel.get_session_id(MODEL_GLOBAL_DICT['github'])


def branch_lister() -> dict:
    """
    branch lister function
    :return:
    """
    return GhBranch.list_all_branches(MODEL_GLOBAL_DICT['github'])


def branch_creator(source_branch_name, target_branch_name) -> dict:
    """
    branch creator function
    :param source_branch_name:
    :param target_branch_name:
    :return:
    """
    return GhBranch.create_branch(MODEL_GLOBAL_DICT['github'],
                                  source_branch=source_branch_name,
                                  target_branch=target_branch_name)


def branch_deleter(branch_name) -> dict:
    """
    branch deleter function
    :param branch_name:
    :return:
    """
    return GhBranch.delete_branch(MODEL_GLOBAL_DICT['github'],
                                  branch_name=branch_name)


def file_lister(branch_name) -> dict:
    """
    file lister function
    :param branch_name:
    :return:
    """
    files_list_response = GhFile.list_all_files(MODEL_GLOBAL_DICT['github'], branch_name)

    if files_list_response.get('status') == 200:
        _files_list = []
        for file in files_list_response.get('content'):
            file_extension = os.path.splitext(str(file))[1]
            if file_extension in settings.EDITABLE_FILE_EXTENSION_LIST:
                _files_list.append([file, True])
            else:
                _files_list.append([file, False])
        files_list_response['content'] = _files_list

    return files_list_response


def file_exists_checker(gh_file_path, branch_name) -> dict:
    """
    file exists checker function
    :param gh_file_path:
    :param branch_name:
    :return:
    """
    return GhFile.get_file_status(MODEL_GLOBAL_DICT['github'],
                                  gh_file_path, branch_name)


def file_content_getter(gh_file_path, branch_name) -> dict:
    """
    file content getter function
    :param gh_file_path:
    :param branch_name:
    :return:
    """
    return GhFile.get_file_contents(MODEL_GLOBAL_DICT['github'],
                                    gh_file_path, branch_name)


def file_creator(gh_file_path, message, content, branch_name) -> dict:
    """
    file creator function
    :param gh_file_path:
    :param message:
    :param content:
    :param branch_name:
    :return:
    """
    return GhFile.create_file(MODEL_GLOBAL_DICT['github'],
                              gh_file_path=gh_file_path,
                              message=message,
                              content=content,
                              branch_name=branch_name)


def file_updater(gh_file_path, message, content, branch_name) -> dict:
    """
    file updater function
    :param gh_file_path:
    :param message:
    :param content:
    :param branch_name:
    :return:
    """
    return GhFile.update_file(MODEL_GLOBAL_DICT['github'],
                              gh_file_path=gh_file_path,
                              message=message,
                              content=content,
                              branch_name=branch_name)


def file_deleter(gh_file_path, message, branch_name) -> dict:
    """
    file deleter function
    :param gh_file_path:
    :param message:
    :param branch_name:
    :return:
    """
    return GhFile.delete_file(MODEL_GLOBAL_DICT['github'],
                              gh_file_path=gh_file_path,
                              message=message,
                              branch_name=branch_name)
