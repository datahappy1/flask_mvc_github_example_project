from github import Github
from flaskr.lib import settings
import requests


class Model:
    """
    project parent github class
    """
    def __init__(self, init_token, init_repo):
        # using username and password
        # g = Github("", "")
        # or using an access token
        self.token = init_token
        self.g = Github(self.token)
        self.repo = self.g.get_repo(init_repo)
        self.repo_folder = settings.repo_folder

    def get_session_id(self):
        return self.g


class Branch(Model):
    def list_all_branches(self):
        branches = self.repo.get_branches()
        branches_list = []
        for branch in branches:
            branches_list.append(str(branch).replace('Branch(name="', '').replace('")', ''))
        return branches_list

    def create_branch(self):
        pass

    def delete_branch(self):
        pass


class File(Model):
    def list_all_files(self, branch_name):
        files = self.repo.get_dir_contents("/flaskr/" + self.repo_folder, ref=branch_name)
        files_list = []
        for file in files:
                files_list.append(str(file).replace('ContentFile(path="', '').replace('")', ''))
        return files_list

    def get_file_status(self, gh_file_path, branch_name):
        contents = self.repo.get_contents(gh_file_path, ref=branch_name)
        url = contents.download_url
        r = requests.get(url)
        return r.status_code

    def get_file_sha(self, gh_file_path, branch_name):
        resp = self.repo.get_contents(gh_file_path, ref=branch_name)
        sha = resp.sha
        return sha

    def get_file_contents(self, gh_file_path, branch_name):
        contents = self.repo.get_contents(gh_file_path, ref=branch_name)
        url = contents.download_url
        r = requests.get(url)
        raw_data = r.content.decode('UTF-8')
        return raw_data

    def create_file(self, gh_file_path, message, content, branch_name):
        self.repo.create_file(gh_file_path, message, content, branch_name)
        return 0

    def update_file(self, gh_file_path, message, content, branch_name):
        sha = File.get_file_sha(self, gh_file_path, branch_name)
        self.repo.update_file(gh_file_path, message, content, sha, branch_name)
        return 0

    def save_file(self, gh_file_path, message, content, branch_name):
        file_status = File.get_file_status(self, gh_file_path, branch_name)
        if file_status == 200:
            File.update_file(self, gh_file_path, message, content, branch_name)
        else:
            File.create_file(self, gh_file_path, message, content, branch_name)
        return 0

    def delete_file(self, gh_file_path, message, branch_name):
        sha = File.get_file_sha(self, gh_file_path, branch_name)
        self.repo.delete_file(gh_file_path, message, sha, branch=branch_name)
        return 0
