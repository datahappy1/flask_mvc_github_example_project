from github import Github
import requests


class GitHubClass:
    """
    project github class
    """
    def __init__(self, init_token, init_repo):
        # using username and password
        # g = Github("", "")
        # or using an access token
        self.token = init_token
        self.g = Github(self.token)
        self.repo = self.g.get_repo(init_repo)

    def get_session_id(self):
        return self.g

    def list_all_branches(self):
        branches = self.repo.get_branches()
        branches_list = []
        for branch in branches:
            branches_list.append(str(branch).replace('Branch(name="', '').replace('")', ''))
        return branches_list

    def list_all_files(self, branch_name):
        files = self.repo.get_dir_contents("/flaskr/files_playground", ref=branch_name)
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
        return r.status_code, raw_data

    def create_file(self, path, message, content, branch_name):
        self.repo.create_file(path, message, content, branch_name)
        return 0

    def update_file(self, path, message, content, branch_name):
        sha = GitHubClass.get_file_sha(self, path, branch_name)
        print(path, message, content, branch_name, sha)
        self.repo.update_file(path, message, content, sha, branch_name)
        return 0

    def save_file(self, path, message, content, gh_file_path, branch_name):
        file_status = GitHubClass.get_file_status(self, gh_file_path, branch_name)
        if file_status == 200:
            GitHubClass.update_file(self, path, message, content, branch_name)
        else:
            GitHubClass.create_file(self, path, message, content, branch_name)
        return 0

    def delete_file(self, path, message, branch_name):
        sha = GitHubClass.get_file_sha(self, path, branch_name)
        self.repo.delete_file(path, message, sha, branch=branch_name)
        return 0