"""
test api endpoints
"""
import pytest
import requests
import os
import uuid

TEST_RUNNER_ID = str(uuid.uuid4())
API_BASE_ENDPOINT = 'http://127.0.0.1:5000/api'


@pytest.mark.parametrize(
    "test_name, method, endpoint, params, expected_success_status_code",[
        # to ensure a unique branch name and filename for our test runner in the repo,
        # concatenate "requests_test_" and the generated test_runner_id uuid var
        ('create branch', 'post', '{}/branch/requests_test_{}/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'branch_name_src': 'master'}, 201),
        ('get branches', 'get', '{}/gh_branches_manager/'.format(API_BASE_ENDPOINT), None, 200),
        ('create file', 'post', '{}/branch/requests_test_{}/file/my-file_{}.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 201),
        ('edit file', 'put', '{}/branch/requests_test_{}/file/my-file_{}.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 201),
        ('get files', 'get', '{}/gh_files_manager/branch/requests_test_{}/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), None, 200),
        ('delete file', 'delete', '{}/branch/requests_test_{}/file/my-file_{}.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 200),
        ('delete branch', 'delete', '{}/branch/requests_test_{}/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), None, 200),
    ])
def test_request(test_name, method, endpoint, params, expected_success_status_code):
    """
    test request function
    :param test_name:
    :param method:
    :param endpoint:
    :param params:
    :param expected_success_status_code:
    :return:
    """
    response, file_content = None, None

    if method == "get":
        response = requests.get(endpoint)

    elif method == "post":
        if test_name == "create branch":
            file_content = None
        elif test_name == "create file":
            # use the test file content as request data located in tests/files/test_file.txt for testing the post method
            with open(os.path.join(os.getcwd(), 'files', 'test_file.txt'), 'rb') as fp:
                file_content = fp.read()
        else:
            raise NotImplementedError

        response = requests.post(endpoint, data=file_content, params=params)

    elif method == "put":
        if test_name == "edit file":
            # use the test file content as request data located in tests/files/test_file.txt for testing the put method
            with open(os.path.join(os.getcwd(), 'files', 'test_file.txt'), 'rb') as fp:
                file_content = fp.read()
        else:
            raise NotImplementedError

        response = requests.put(endpoint, data=file_content, params=params)

    elif method == "delete":
        response = requests.delete(endpoint, params=params)

    assert response.status_code == expected_success_status_code
