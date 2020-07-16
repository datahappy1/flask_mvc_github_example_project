"""
model github module
"""
import requests

from github import Github, GithubException
from flaskr import settings


class GhBaseModel:
    """
    project parent github class
    """

    def __init__(self, init_token, init_repo):
        self.github = Github(init_token)
        self.repo = self.github.get_repo(init_repo)
        self.repo_folder = settings.REPO_FOLDER

    def __repr__(self):
        return "{}, {}".format(self.github, id(self))

    def get_session_id(self) -> dict:
        """
        get session id function
        :return:
        """
        try:
            return {'status': 200,
                    'content': self.github}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}


class GhBranch(GhBaseModel):
    """
    Model subclass Branch
    """

    def list_all_branches(self) -> dict:
        """
        list all branches function
        :return:
        """
        try:
            branches_response = self.repo.get_branches()
            branches_list = []
            for branch in branches_response:
                branches_list.append(branch.raw_data.get('name'))
            return {'status': 200,
                    'content': branches_list}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def create_branch(self, source_branch, target_branch) -> dict:
        """
        create branch function
        :param source_branch:
        :param target_branch:
        :return:
        """
        try:
            src_branch_response = self.repo.get_branch(source_branch)
            self.repo.create_git_ref(ref='refs/heads/' + target_branch,
                                     sha=src_branch_response.commit.sha)
            return {'status': 201}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def delete_branch(self, branch_name) -> dict:
        """
        delete branch function
        :param branch_name:
        :return:
        """
        try:
            branch_ref_response = self.repo.get_git_ref(f"heads/{branch_name}")
            branch_ref_response.delete()
            return {'status': 200}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}


class GhFile(GhBaseModel):
    """
    Model subclass File
    """

    def list_all_files(self, branch_name) -> dict:
        """
        list all files function
        :param branch_name:
        :return:
        """
        try:
            files_response = self.repo.get_contents(self.repo_folder,
                                                    ref=branch_name)
            files_list = []
            for file in files_response:
                files_list.append(file.raw_data.get('path'))
            return {'status': 200,
                    'content': files_list}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def get_head_commit(self, branch_name) -> dict:
        """
        get head commit function (needed to get latest file contents)
        :param branch_name:
        :return:
        """
        try:
            commit_response = self.repo.get_branch(branch_name)
            commit = commit_response.commit
            commit_head = commit.raw_data.get('sha')
            return {'status': 200,
                    'content': commit_head}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def get_file_status(self, gh_file_path, branch_name) -> dict:
        """
        get file status function
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        try:
            contents_response = self.repo.get_contents(gh_file_path, ref=branch_name)
            url = contents_response.download_url
            request_response = requests.get(url)
            return {'status': 200,
                    'content': request_response.status_code}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def get_file_sha(self, gh_file_path, branch_name) -> dict:
        """
        get file sha function
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        try:
            sha_response = self.repo.get_contents(gh_file_path, ref=branch_name)
            sha = sha_response.sha
            return {'status': 200,
                    'content': sha}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def get_file_contents(self, gh_file_path, branch_name) -> dict:
        """
        get file contents function
        :param gh_file_path:
        :param branch_name:
        :return:
        """
        try:
            commit_response = GhFile.get_head_commit(self, branch_name)
            if commit_response.get('status') == 200:
                ref = commit_response.get('content')
            # if cannot retrieve head commit sha, use branch sha
            else:
                ref = branch_name

            contents_response = self.repo.get_contents(gh_file_path, ref=ref)
            url = contents_response.download_url
            request_response = requests.get(url)
            raw_data = request_response.content.decode('UTF-8')
            return {'status': 200,
                    'content': raw_data}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def create_file(self, gh_file_path, message, content, branch_name) -> dict:
        """
        create file function
        :param gh_file_path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        try:
            self.repo.create_file(gh_file_path, message, content, branch_name)
            return {'status': 201}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}

    def update_file(self, gh_file_path, message, content, branch_name) -> dict:
        """
        update file function
        :param gh_file_path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        sha_response = GhFile.get_file_sha(self, gh_file_path, branch_name)
        if sha_response.get('status') == 200:
            sha = sha_response.get('content')
            try:
                self.repo.update_file(gh_file_path, message, content, sha, branch_name)
                return {'status': 200}
            except GithubException as github_exc:
                return {'status': github_exc.status,
                        'error': github_exc.data}
        else:
            return {'status': sha_response.get('status'),
                    'error': sha_response.get('error')}

    def delete_file(self, gh_file_path, message, branch_name) -> dict:
        """
        delete file function
        :param gh_file_path:
        :param message:
        :param branch_name:
        :return:
        """
        sha_response = GhFile.get_file_sha(self, gh_file_path, branch_name)
        if sha_response.get('status') == 200:
            sha = sha_response.get('content')
            try:
                self.repo.delete_file(gh_file_path, message, sha,
                                      branch=branch_name)
                return {'status': 200}
            except GithubException as github_exc:
                return {'status': github_exc.status,
                        'error': github_exc.data}
        else:
            return {'status': sha_response.get('status'),
                    'error': sha_response.get('error')}
