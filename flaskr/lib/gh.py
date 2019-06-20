from github import Github
import requests


class GitHubClass:
    """
    project github class
    """
    def __init__(self, init_token, init_repo, init_branch_name, init_local_file_path):
        # using username and password
        # g = Github("", "")
        # or using an access token
        self.token = init_token
        self.g = Github(self.token)
        self.repo = self.g.get_repo(init_repo)
        self.branch_name = init_branch_name
        self.local_file_path = init_local_file_path

    def get_session_id(self):
        """
        get session id for testing
        :return:
        """
        return self.g

    def list_all_branches(self):
        """
        list all github repo branches
        :return:
        """
        branches = self.repo.get_branches()
        branches_list = []
        for branch in branches:
            branches_list.append(str(branch).replace('Branch(name="', '').replace('")', ''))
        return branches_list

    def list_all_files(self):
        """
        list all files_playground in a github repo branch
        :return:
        """
        files = self.repo.get_contents("files_playground", ref=self.branch_name)
        files_list = []
        for file in files:
            files_list.append(str(file).replace('ContentFile(path="', '').replace('")', ''))
        return files_list

    def get_file(self):
        """
        get contents of a file in a github repo
        :return:
        """
        contents = self.repo.get_contents("files_playground/test.json", ref=self.branch_name)
        url = contents.download_url
        r = requests.get(url)
        f_path = self.local_file_path
        with open(f_path, 'wb') as f:
            f.write(r.content)
        return r.status_code, f_path

    def create_file(self):
        """
        create a file in a github repo
        :return:
        """
        self.repo.create_file("test.txt", "test", "test", branch=self.branch_name)
        return 0

    def update_file(self):
        """
        update a file in a github repo
        :return:
        """
        contents = self.repo.get_contents("test.txt", ref="test")
        self.repo.update_file(contents.path, "more tests", "more tests", contents.sha, branch=self.branch_name)
        return 0
