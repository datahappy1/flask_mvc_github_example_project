"""
test api endpoints
"""
import uuid
import os

from flaskr.settings import API_BASE_ENDPOINT
from flaskr.app import APP

TEST_RUNNER_ID = uuid.uuid4()
TEST_BRANCH_NAME = 'requests_test_{}'.format(TEST_RUNNER_ID)
TEST_FILE_NAME = 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'


def test_request_create_branch():
    test_case_endpoint = '{}/branches'.format(API_BASE_ENDPOINT)
    test_case_params = {'branch_name_tgt': TEST_BRANCH_NAME, 'branch_name_src': 'master'}
    test_case_expected_status_code = 201

    response = APP.test_client().post(test_case_endpoint,
                                      data=test_case_params)

    assert response.status_code == test_case_expected_status_code


def test_request_get_branches():
    test_case_endpoint = '{}/branches'.format(API_BASE_ENDPOINT)
    test_case_expected_status_code = 200

    response = APP.test_client().get(test_case_endpoint)

    assert response.status_code == test_case_expected_status_code


def test_request_create_file1_upload():
    test_case_endpoint = '{}/branches/{}/files'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME)
    test_case_params = {'commit_message': 'pytest'}
    test_case_expected_status_code = 201

    with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
        data = test_case_params
        data['uploaded_file'] = (fp, fp.name)
        response = APP.test_client().post(test_case_endpoint,
                                          content_type="multipart/form-data",
                                          data=data)

    assert response.status_code == test_case_expected_status_code


def test_request_edit_file1():
    test_case_endpoint ='{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME)
    test_case_params = {'commit_message': 'pytest'}
    test_case_expected_status_code = 200

    with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
        file_content = fp.read()
        data = test_case_params
        data['file_contents'] = file_content
        response = APP.test_client().put(test_case_endpoint,
                                         data=data)

    assert response.status_code == test_case_expected_status_code


def test_request_delete_file1():
    test_case_endpoint ='{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME)
    test_case_params = {'commit_message': 'pytest'}
    test_case_expected_status_code = 200

    response = APP.test_client().delete(test_case_endpoint,
                                        data=test_case_params)

    assert response.status_code == test_case_expected_status_code


def test_request_create_file2_form():
    test_case_endpoint = '{}/branches/{}/files'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME)
    test_case_params = {'commit_message': 'pytest', 'file_name': TEST_FILE_NAME}
    test_case_expected_status_code = 201

    with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
        file_content = fp.read()
        data = test_case_params
        data['file_contents'] = file_content
        response = APP.test_client().post(test_case_endpoint,
                                          data=data)

    assert response.status_code == test_case_expected_status_code


def test_request_override_file2():
    test_case_endpoint ='{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME)
    test_case_params = {'commit_message': 'pytest'}
    test_case_expected_status_code = 200

    with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
        data = test_case_params
        data['uploaded_file'] = (fp, fp.name)
        response = APP.test_client().put(test_case_endpoint,
                                         content_type="multipart/form-data",
                                         data=data)

    assert response.status_code == test_case_expected_status_code


def test_request_get_files():
    test_case_endpoint = '{}/branches/{}/files'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME)
    test_case_expected_success_status_code = 200

    response = APP.test_client().get(test_case_endpoint)
    assert response.status_code == test_case_expected_success_status_code


def test_request_delete_file2():
    test_case_endpoint = '{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME)
    test_case_params = {'commit_message': 'pytest'}
    test_case_expected_status_code = 200

    response = APP.test_client().delete(test_case_endpoint,
                                        data=test_case_params)

    assert response.status_code == test_case_expected_status_code


def test_request_delete_branch():
    test_case_endpoint = '{}/branches/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME)
    test_case_params = {}
    test_case_expected_status_code = 200

    response = APP.test_client().delete(test_case_endpoint,
                                        data=test_case_params)

    assert response.status_code == test_case_expected_status_code
