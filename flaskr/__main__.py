import os
from flask import Flask, render_template, request, redirect, flash
from flaskr.lib import gh, settings

# github related variables
token = os.environ['token']
# branch_name and local_file_path is temporary for testing
repo = settings.repo
branch_name = "dev"
local_file_path = os.getcwd().rstrip('lib') + os.path.join('files_playground', 'temp', 'test_' + branch_name + '.json')

# init the github class
obj = gh.GitHubClass(init_token=token, init_repo=repo, init_branch_name=branch_name,
                     init_local_file_path=local_file_path)

# flask app starts here
app = Flask(__name__)
app.secret_key = 'abcd1234'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gh_files_manager')
def gh_files_manager():
    gh_session_id = gh.GitHubClass.get_session_id(obj)
    branch_list = gh.GitHubClass.list_all_branches(obj)
    files_list = gh.GitHubClass.list_all_files(obj)

    return render_template('gh_files_manager.html', gh_session_id=gh_session_id,
                           b_list=branch_list, curr_branch=branch_name, f_list=files_list)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(temp_file_path + f.filename)
        flash(f.filename + ' was uploaded!')
        return redirect('/config')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
