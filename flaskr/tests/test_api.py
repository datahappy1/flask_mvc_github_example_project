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
        ('create branch', 'post', '{}/branch/'.format(API_BASE_ENDPOINT), {'branch_name_tgt': 'requests_test_{}'.format(TEST_RUNNER_ID), 'branch_name_src': 'master'}, 201),
        ('get branches', 'get', '{}/gh_branches_manager/'.format(API_BASE_ENDPOINT), None, 200),
        ('create file upload', 'post', '{}/branch/requests_test_{}/file/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 201),
        ('edit file', 'put', '{}/branch/requests_test_{}/file/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 201),
        ('delete file', 'delete','{}/branch/requests_test_{}/file/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 200),
        ('create file form', 'post', '{}/branch/requests_test_{}/file/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'commit_message': 'pytest', 'file_name': 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'}, 201),
        ('override file', 'put', '{}/branch/requests_test_{}/file/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 201),
        ('get files', 'get', '{}/gh_files_manager/branch/requests_test_{}/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), None, 200),
        ('delete file', 'delete', '{}/branch/requests_test_{}/file/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt/'.format(API_BASE_ENDPOINT, TEST_RUNNER_ID), {'commit_message': 'pytest'}, 200),
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
            response = requests.post(endpoint, data=params)

        elif test_name == "create file upload":
            # use the test file content as request data located in tests/files/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt for testing the post method
            with open(os.path.join(os.getcwd(), 'files', 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'), 'rb') as fp:
                files = {'uploaded_file': fp}
                response = requests.post(endpoint, files=files, data=params)

        elif test_name == "create file form":
            # use the test file content as request data located in tests/files/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt for testing the post method
            with open(os.path.join(os.getcwd(), 'files', 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'), 'rb') as fp:
                file_content = fp.read()
                data = params
                data['file_contents'] = file_content
                response = requests.post(endpoint, data=data)

        else:
            raise NotImplementedError

    elif method == "put":
        if test_name == "edit file":
            # use the test file content as request data located in tests/files/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt for testing the put method
            with open(os.path.join(os.getcwd(), 'files', 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'), 'rb') as fp:
                file_content = fp.read()
                data = params
                data['file_contents'] = file_content
                response = requests.put(endpoint, data=data)

        elif test_name == "override file":
            # use the test file content as request data located in tests/files/test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt for testing the put method
            with open(os.path.join(os.getcwd(), 'files', 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'), 'rb') as fp:
                files = {'uploaded_file': fp}
                response = requests.put(endpoint, files=files, data=params)

        else:
            raise NotImplementedError

    elif method == "delete":
        response = requests.delete(endpoint, data=params)

    assert response.status_code == expected_success_status_code
