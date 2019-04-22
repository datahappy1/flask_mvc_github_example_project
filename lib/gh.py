from github import Github
import requests

# https://pygithub.readthedocs.io/en/latest/examples.html
# https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line


class GitHubClass:
    def __init__(self, init_token, init_repo, init_branch_name, init_local_file_path):
        # using username and password
        #g = Github("", "")
        # or using an access token
        self.token = init_token
        self.g = Github(self.token)
        self.repo = self.g.get_repo(init_repo)
        self.branch_name = init_branch_name
        self.local_file_path = init_local_file_path

    def get_session_id(self):
        return self.g

    def list_all_branches(self):
        branches = self.repo.get_branches()
        branches_list = []
        for branch in branches:
            branches_list.append(str(branch).replace('Branch(name="', '').replace('")', ''))
        return branches_list

    def list_all_files(self):
        files = self.repo.get_contents("files", ref=self.branch_name)
        files_list = []
        for file in files:
            files_list.append(str(file).replace('ContentFile(path="', '').replace('")', ''))
        return files_list

    def get_file(self):
        contents = self.repo.get_contents("files/test.json", ref=self.branch_name)
        url = contents.download_url
        r = requests.get(url)
        f_path = self.local_file_path
        with open(f_path, 'wb') as f:
            f.write(r.content)
        # Retrieve HTTP meta-data
        # print(r.status_code)
        # print(r.headers['content-type'])
        # print(r.encoding)
        return r.status_code, f_path

    def create_file(self):
        self.repo.create_file("test.txt", "test", "test", branch=self.branch_name)
        return 0

    def update_file(self):
        contents = self.repo.get_contents("test.txt", ref="test")
        self.repo.update_file(contents.path, "more tests", "more tests", contents.sha, branch=self.branch_name)
        return 0


#token = "978ea3d99448d749df792b9bf3487c43fc753756"
#repo = "datahappy1/flask_github_integrator"
#branch_name = "dev"
#local_file_path = os.getcwd().rstrip('lib') + os.path.join('\\files', 'temp', 'test_' + branch_name + '.json')


#obj = GitHubClass(init_token=token, init_repo=repo, init_branch_name=branch_name, init_local_file_path=local_file_path)
#x = GitHubClass.list_all_branches(obj)
#x = GitHubClass.list_all_files(obj)
#x = GitHubClass.get_session_id(obj)
#print(x)
