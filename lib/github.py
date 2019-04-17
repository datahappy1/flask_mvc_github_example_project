from github import Github
import requests
import os


class GitHubClass:
    def __init__(self):
        # using username and password
        #g = Github("yourAccount", "yourPassword")

        # or using an access token
        g = Github("")
        # https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line

        self.repo = g.get_repo("datahappy1/flask_github_integrator")
        self.branch_name = "dev"
        self.fpath = os.getcwd().rstrip('lib') + os.path.join('files', 'temp', 'test_' + self.branch_name + '.json')

    def list_branches(self):
        return list(self.repo.get_branches())

    def get_file(self):
        contents = self.repo.get_contents("files/test.json", ref=self.branch_name)
        url = contents.download_url
        # print(url)
        print('Beginning file download with requests')
        r = requests.get(url)

        fpath = self.fpath
        # print(fpath)
        with open(fpath, 'wb') as f:
            f.write(r.content)

        # Retrieve HTTP meta-data
        #print(r.status_code)
        #print(r.headers['content-type'])
        #print(r.encoding)

        return r.status_code, fpath

    def put_file(self):
        pass



obj = GitHubClass()
lb = GitHubClass.list_branches(obj)
print(lb)