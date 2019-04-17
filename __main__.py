import os
import pandas as pd
from flask import Flask, render_template
from lib import gh

app = Flask(__name__)


@app.route('/index/')
def index():
    obj = gh.GitHubClass()
    resp, fpath = gh.GitHubClass.get_file(obj)
    fpath = "C:\\flask_github_integrator\\files\\temp\\test_dev.json"
    if resp:
        with open(fpath, "r") as f:
            data = f.read()
        #print(data)

        data = dict(data)
        print(data)

        df = pd.DataFrame(data)
    else:
        raise Exception

    return render_template('index.html', fname=fpath, tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
