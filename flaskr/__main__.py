import os
from flask import Flask, render_template, request, redirect, flash, session
from flaskr.lib import gh, settings

# github related variables
token = os.environ['token']
repo = settings.repo
repo_folder = settings.repo_folder
init_branch_name = settings.initial_branch_name

# init the github class
obj = gh.GitHubClass(init_token=token, init_repo=repo, init_branch_name=init_branch_name)

# flask app starts here
app = Flask(__name__)
app.secret_key = 'abcd1234'


@app.route('/')
def index():
    return render_template('index.html',
                           template_current_branch=init_branch_name)


@app.route('/views/gh_files_manager/branch/<branch_name>', methods=['GET', 'POST'])
def gh_files_manager(branch_name):
    gh_session_id = gh.GitHubClass.get_session_id(obj)
    branch_list = gh.GitHubClass.list_all_branches(obj)
    files_list = gh.GitHubClass.list_all_files(obj)

    return render_template('views/gh_files_manager.html',
                           gh_session_id=gh_session_id,
                           template_branch_list=branch_list,
                           template_current_branch=branch_name,
                           template_file_list=files_list)


@app.route('/upload')
def upload():
    return render_template('templates/upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(temp_file_path + f.filename)
        flash(f.filename + ' was uploaded!')
        return redirect('/config')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', threaded=True)
