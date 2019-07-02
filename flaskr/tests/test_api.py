"""
test api endpoints
"""
import pytest
import requests


@pytest.mark.parametrize(
    "test_name, method, endpoint, expected_success_status_code",[
        ('create branch', 'post', 'http://127.0.0.1:5000/api/branch/requests_test?branch_name_src=master', 201),
        ('get branches', 'get', 'http://127.0.0.1:5000/api/gh_branches_manager/', 200),
        ('create file', 'post', 'http://127.0.0.1:5000/api/branch/requests_test/my-file.txt?commit_message="pytest"', 200),
        ('edit file', 'put', 'http://127.0.0.1:5000/api/branch/master/my-file.txt?commit_message="pytest"', 200),
        ('get files', 'get', 'http://127.0.0.1:5000/api/gh_files_manager/branch/requests_test/', 200),
        ('delete file', 'delete', 'http://127.0.0.1:5000/api/branch/requests_test/my-file.txt?commit_message="pytest"', 200),
        ('delete branch', 'delete', 'http://127.0.0.1:5000/api/branch/requests_test/', 200),
    ])
def test_request(test_name, method, endpoint, expected_success_status_code):
    print(test_name)

    if method == "get":
        response = requests.get(endpoint)
    elif method == "post":
        response = requests.get(endpoint)
    elif method == "put":
        response = requests.get(endpoint)
    elif method == "delete":
        response = requests.get(endpoint)

    assert response.status_code == expected_success_status_code
