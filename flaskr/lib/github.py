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

    def list_all_files(self, branch_name):
        """
        list all files_playground in a github repo branch
        :return:
        """
        # files = self.repo.get_contents("/flaskr/files_playground", ref=self.branch_name)
        files = self.repo.get_dir_contents("/flaskr/files_playground", ref=branch_name)
        files_list = []
        for file in files:
                files_list.append(str(file).replace('ContentFile(path="', '').replace('")', ''))
        return files_list

    def download_file(self, branch_name):
        """
        get contents of a file in a github repo
        :return:
        """
        contents = self.repo.get_contents("files_playground/test.json", ref=branch_name)
        url = contents.download_url
        r = requests.get(url)
        f_path = self.local_file_path
        with open(f_path, 'wb') as f:
            f.write(r.content)
        return r.status_code, f_path

    def get_file_contents(self, gh_file_path, branch_name):
        """
        get contents of a file in a github repo
        :return:
        """
        contents = self.repo.get_contents(gh_file_path, ref=branch_name)
        url = contents.download_url
        r = requests.get(url)
        return r.status_code, r.content

    def create_file(self, path, message, content, branch_name):
        """
        create a file in a github repo
        :param path:
        :param message:
        :param content:
        :param branch_name:
        :return:
        """
        self.repo.create_file(path=path, message=message, content=content, branch=branch_name)
        return 0

    def update_file(self, branch_name):
        """
        update a file in a github repo
        :return:
        """
        contents = self.repo.get_contents("test.txt", ref="test")
        self.repo.update_file(contents.path, "more tests", "more tests", contents.sha, branch=branch_name)
        return 0
