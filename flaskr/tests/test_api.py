"""
test api endpoints
"""
import pytest
import requests
import os

@pytest.mark.parametrize(
    "test_name, method, endpoint, params, expected_success_status_code",[
        # to ensure a unique branch name and filename for our test runner in the repo,
        # concatenate "requests_test_" and this uuid "_51568f0d-5dc4-4f88-b53a-a7a3476203db"
        ('create branch', 'post', 'http://127.0.0.1:5000/api/branch/requests_test_51568f0d-5dc4-4f88-b53a-a7a3476203db/', {'branch_name_src': 'master'}, 201),
        ('get branches', 'get', 'http://127.0.0.1:5000/api/gh_branches_manager/', None, 200),
        ('create file', 'post', 'http://127.0.0.1:5000/api/branch/requests_test_51568f0d-5dc4-4f88-b53a-a7a3476203db/file/my-file_51568f0d-5dc4-4f88-b53a-a7a3476203db.txt/', {'commit_message': 'pytest'} , 201),
        ('edit file', 'put', 'http://127.0.0.1:5000/api/branch/requests_test_51568f0d-5dc4-4f88-b53a-a7a3476203db/file/my-file_51568f0d-5dc4-4f88-b53a-a7a3476203db.txt/', {'commit_message': 'pytest'}, 201),
        ('get files', 'get', 'http://127.0.0.1:5000/api/gh_files_manager/branch/requests_test_51568f0d-5dc4-4f88-b53a-a7a3476203db/', None, 200),
        ('delete file', 'delete', 'http://127.0.0.1:5000/api/branch/requests_test_51568f0d-5dc4-4f88-b53a-a7a3476203db/file/my-file_51568f0d-5dc4-4f88-b53a-a7a3476203db.txt/', {'commit_message': 'pytest'}, 200),
        ('delete branch', 'delete', 'http://127.0.0.1:5000/api/branch/requests_test_51568f0d-5dc4-4f88-b53a-a7a3476203db/', None, 200),
    ])
def test_request(test_name, method, endpoint, params, expected_success_status_code):
    response, file_content = None, None

    if method == "get":
        response = requests.get(endpoint)

    elif method == "post":
        if test_name == "create branch":
            file_content = None
        elif test_name == "create file":
            # use the test file content as request data located in tests/files/test_file.txt for testing the post method
            with open(os.path.join(os.getcwd(), 'files', 'test_file.txt')) as fp:
                file_content = fp.read()
        else:
            raise NotImplementedError

        response = requests.post(endpoint, data=file_content, params=params)

    elif method == "put":
        if test_name == "edit file":
            # use the test file content as request data located in tests/files/test_file.txt for testing the put method
            with open(os.path.join(os.getcwd(), 'files', 'test_file.txt')) as fp:
                file_content = fp.read()
        else:
            raise NotImplementedError

        response = requests.put(endpoint, data=file_content, params=params)

    elif method == "delete":
        response = requests.delete(endpoint, params=params)

    assert response.status_code == expected_success_status_code
