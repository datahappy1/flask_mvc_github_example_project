"""
model module
"""
import os

from flaskr import settings

class Model:
    """
    Base Model class
    """

    def __init__(self, concrete_model):
        self.model = concrete_model

    def get_session_id(self) -> dict:
        """
        get_session_id method
        :return:
        """
        return self.model.get_session_id()

    def list_all_branches(self) -> dict:
        """
        list_all_branches method
        :return:
        """
        return self.model.list_all_branches()

    def create_branch(self, source_branch_name, target_branch_name) -> dict:
        """
        create_branch method
        :param source_branch_name:
        :param target_branch_name:
        :return:
        """
        return self.model.create_branch(
            source_branch=source_branch_name,
            target_branch=target_branch_name
        )

    def delete_branch(self, branch_name) -> dict:
        """
        delete_branch method
        :param branch_name:
        :return:
        """
        return self.model.delete_branch(
            branch_name=branch_name
        )

    def list_all_files(self, branch_name) -> dict:
        """
        list_all_files method
        :param branch_name:
        :return:
        """
        files_list_response = self.model.list_all_files(
            branch_name
        )

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

    def get_file_status(self, gh_file_path, branch_name) -> dict:
        """
        get_file_status method
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        return self.model.get_file_status(
            gh_file_path, branch_name
        )

    def get_file_contents(self, gh_file_path, branch_name) -> dict:
        """
        get_file_contents method
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        return self.model.get_file_contents(
            gh_file_path, branch_name
        )

    def create_file(self, gh_file_path, message, content, branch_name) -> dict:
        """
        create_file method
        :param gh_file_path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        return self.model.create_file(
            gh_file_path=gh_file_path,
            message=message,
            content=content,
            branch_name=branch_name
        )

    def update_file(self, gh_file_path, message, content, branch_name) -> dict:
        """
        update_file method
        :param gh_file_path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        return self.model.update_file(
            gh_file_path=gh_file_path,
            message=message,
            content=content,
            branch_name=branch_name
        )

    def delete_file(self, gh_file_path, message, branch_name) -> dict:
        """
        delete_file method
        :param gh_file_path:
        :param message:
        :param branch_name:
        :return:
        """
        return self.model.delete_file(
            gh_file_path=gh_file_path,
            message=message,
            branch_name=branch_name
        )
