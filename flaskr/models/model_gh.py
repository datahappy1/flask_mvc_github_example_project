"""
model github module
"""
import requests

from github import Github, GithubException
from flaskr.project_variables import settings


class Model:  # pylint: disable=too-few-public-methods
    """
    project parent github class
    """
    def __init__(self, init_token, init_repo):
        # using username and password
        # g = Github("", "")
        # or using an access token
        self.token = init_token
        self.github = Github(self.token)
        self.repo = self.github.get_repo(init_repo)
        self.repo_folder = settings.REPO_FOLDER

    def get_session_id(self) -> dict:
        """
        get session id function
        :return:
        """
        return {'status': 200,
                'content': self.github}


class Branch(Model):
    """
    Model subclass Branch
    """
    def list_all_branches(self) -> dict:
        """
        list all branches function
        :return:
        """
        try:
            branches = self.repo.get_branches()
            branches_list = []
            for branch in branches:
                branches_list.append(str(branch)
                                     .replace('Branch(name="', '')
                                     .replace('")', ''))
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
            srcbranch = self.repo.get_branch(source_branch)
            self.repo.create_git_ref(ref='refs/heads/' + target_branch,
                                     sha=srcbranch.commit.sha)
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
            branch_ref = self.repo.get_git_ref(f"heads/{branch_name}")
            branch_ref.delete()
            return {'status': 200}
        except GithubException as github_exc:
            return {'status': github_exc.status,
                    'error': github_exc.data}


class File(Model):
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
            files = self.repo.get_dir_contents("/flaskr/" + self.repo_folder,
                                               ref=branch_name)
            files_list = []
            for file in files:
                files_list.append(str(file).
                                  replace('ContentFile(path="', '').
                                  replace('")', ''))
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
            _commit = self.repo.get_branch(branch_name)
            commit = _commit.commit
            commit = str(commit).replace('Commit(sha="', '').replace('")', '')
            return {'status': 200,
                    'content': commit}
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
            contents = self.repo.get_contents(gh_file_path, ref=branch_name)
            url = contents.download_url
            req = requests.get(url)
            return {'status': 200,
                    'content': req.status_code}
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
            resp = self.repo.get_contents(gh_file_path, ref=branch_name)
            sha = resp.sha
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
            _commit = File.get_head_commit(self, branch_name)
            if _commit.get('status') == 200:
                ref = _commit.get('content')
            # if cannot retrieve head commit sha, use branch sha
            else:
                ref = branch_name

            contents = self.repo.get_contents(gh_file_path, ref=ref)
            url = contents.download_url
            req = requests.get(url)
            raw_data = req.content.decode('UTF-8')
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
        _sha = File.get_file_sha(self, gh_file_path, branch_name)
        if _sha.get('status') == 200:
            sha = _sha.get('content')
            try:
                self.repo.update_file(gh_file_path, message, content, sha, branch_name)
                return {'status': 200}
            except GithubException as github_exc:
                return {'status': github_exc.status,
                        'error': github_exc.data}
        else:
            return {'status': _sha.get('status'),
                    'error': _sha.get('error')}

    def delete_file(self, gh_file_path, message, branch_name) -> dict:
        """
        delete file function
        :param gh_file_path:
        :param message:
        :param branch_name:
        :return:
        """
        _sha = File.get_file_sha(self, gh_file_path, branch_name)
        if _sha.get('status') == 200:
            sha = _sha.get('content')
            try:
                self.repo.delete_file(gh_file_path, message, sha,
                                      branch=branch_name)
                return {'status': 200}
            except GithubException as github_exc:
                return {'status': github_exc.status,
                        'error': github_exc.data}
        else:
            return {'status': _sha.get('status'),
                    'error': _sha.get('error')}
