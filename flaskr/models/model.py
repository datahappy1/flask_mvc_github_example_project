"""
model module
"""
import os

from flask import current_app

from flaskr import settings
from flaskr.models.model_gh import GhBaseModel, GhBranch, GhFile


class Model:
    """
    Model base class
    """

    def __init__(self):
        self.model = current_app.config["model_github"]

    def session_getter(self) -> dict:
        """
        session getter method
        :return:
        """
        return GhBaseModel.get_session_id(self.model)

    def branch_lister(self) -> dict:
        """
        branch lister method
        :return:
        """
        return GhBranch.list_all_branches(self.model)

    def branch_creator(self, source_branch_name, target_branch_name) -> dict:
        """
        branch creator method
        :param source_branch_name:
        :param target_branch_name:
        :return:
        """
        return GhBranch.create_branch(self.model,
                                      source_branch=source_branch_name,
                                      target_branch=target_branch_name)

    def branch_deleter(self, branch_name) -> dict:
        """
        branch deleter method
        :param branch_name:
        :return:
        """
        return GhBranch.delete_branch(self.model,
                                      branch_name=branch_name)

    def file_lister(self, branch_name) -> dict:
        """
        file lister method
        :param branch_name:
        :return:
        """
        files_list_response = GhFile.list_all_files(self.model,
                                                    branch_name)

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

    def file_exists_checker(self, gh_file_path, branch_name) -> dict:
        """
        file exists checker method
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        return GhFile.get_file_status(self.model,
                                      gh_file_path, branch_name)

    def file_content_getter(self, gh_file_path, branch_name) -> dict:
        """
        file content getter method
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        return GhFile.get_file_contents(self.model,
                                        gh_file_path, branch_name)

    def file_creator(self, gh_file_path, message, content, branch_name) -> dict:
        """
        file creator method
        :param gh_file_path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        return GhFile.create_file(self.model,
                                  gh_file_path=gh_file_path,
                                  message=message,
                                  content=content,
                                  branch_name=branch_name)

    def file_updater(self, gh_file_path, message, content, branch_name) -> dict:
        """
        file updater method
        :param gh_file_path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        return GhFile.update_file(self.model,
                                  gh_file_path=gh_file_path,
                                  message=message,
                                  content=content,
                                  branch_name=branch_name)

    def file_deleter(self, gh_file_path, message, branch_name) -> dict:
        """
        file deleter method
        :param gh_file_path:
        :param message:
        :param branch_name:
        :return:
        """
        return GhFile.delete_file(self.model,
                                  gh_file_path=gh_file_path,
                                  message=message,
                                  branch_name=branch_name)
