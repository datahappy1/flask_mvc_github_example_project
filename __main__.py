import os
from flask import Flask, render_template
from lib import gh, settings

token = os.environ['token']

# branch_name and local_file_path is temporary for testing
repo = settings.repo
branch_name = "dev"
local_file_path = os.getcwd().rstrip('lib') + os.path.join('\\files', 'temp', 'test_' + branch_name + '.json')

obj = gh.GitHubClass(init_token=token, init_repo=repo, init_branch_name=branch_name,
                     init_local_file_path=local_file_path)

app = Flask(__name__)


@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/config')
def config():
    gh_session_id = gh.GitHubClass.get_session_id(obj)
    b_list = gh.GitHubClass.list_all_branches(obj)
    f_list = gh.GitHubClass.list_all_files(obj)

    return render_template('config.html', gh_session_id=gh_session_id,
                           b_list=b_list, curr_branch=branch_name, f_list=f_list)


@app.route('/workflow')
def workflow():
    return render_template('workflow.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
