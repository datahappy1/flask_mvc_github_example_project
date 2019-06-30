import os
from flaskr.lib import global_variables, settings
from flaskr.models import model_gh
from github import GithubException

# controller helper functions returning values only
def session_getter() -> list:
    try:
        session_id = []
        github_session_id = model_gh.Model.get_session_id(global_variables.obj)
        session_id.append(str(github_session_id))
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'session_getter(), '
                f'exception: {str(ge)}']
    return session_id


def branch_lister() -> list:
    try:
        branch_list = model_gh.Branch.list_all_branches(global_variables.obj)
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'branch_lister(), '
                f'exception: {str(ge)}']
    return branch_list


def file_lister(branch_name) -> list:
    try:
        _files_list = model_gh.File.list_all_files(global_variables.obj, branch_name)
        files_list = []
        for file in _files_list:
            file_extension = os.path.splitext(str(file))[1]
            if file_extension in settings.editable_file_extensions_list:
                files_list.append([file, True])
            else:
                files_list.append([file, False])
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'file_lister({branch_name}), '
                f'exception: {str(ge)}']
    return files_list


def file_exists_checker(gh_file_path, branch_name) -> list:
    try:
        file_status = []
        github_file_status = model_gh.File.get_file_status(global_variables.obj, gh_file_path, branch_name)
        file_status.append(github_file_status)
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'file_exists_checker({gh_file_path},{branch_name}),'
                f'exception: {str(ge)}']
    return file_status


def file_content_getter(gh_file_path, branch_name) -> list:
    try:
        file_content = []
        github_file_content = model_gh.File.get_file_contents(global_variables.obj, gh_file_path, branch_name)
        file_content.append(github_file_content)
    except GithubException as ge:
        return [f'Github Exception raised in function {str(__name__)}.'
                f'file_exists_checker({gh_file_path},{branch_name}), '
                f'exception: {str(ge)}']
    return file_content

