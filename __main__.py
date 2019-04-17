import os
from flask import Flask
from flask import Response

app = Flask(__name__)


@app.route('/')
def returner():
    os.chdir("..")
    path = os.path.abspath(os.curdir) + os.path.join(os.sep, 'files', 'temp', 'test_dev.json')

    with open(path, "r") as f:
        data = f.read()
        resp = Response(response=data, status=200, mimetype="application/json")
        return resp


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
