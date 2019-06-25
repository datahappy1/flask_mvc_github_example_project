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

    def get_file_contents(self, gh_file_path, branch_name):
        contents = self.repo.get_contents(gh_file_path, ref=branch_name)
        url = contents.download_url
        r = requests.get(url)
        raw_data = r.content.decode('UTF-8')
        return r.status_code, raw_data

    def create_file(self, path, message, content, branch_name):
        self.repo.create_file(path=path, message=message, content=content, branch=branch_name)
        return 0

    def update_file(self, path, message, content, branch_name):
        resp = self.repo.get_contents(path, ref=branch_name)
        sha = resp.sha
        self.repo.update_file(path, message, content, sha)
        return 0

    def save_file(self):
        pass
        # TODO

    def delete_file(self):
        pass
        # TODO
        #contents = repo.get_contents("test.txt", ref="test")
        #self.repo.delete_file(contents.path, "remove test", contents.sha, branch="test")
