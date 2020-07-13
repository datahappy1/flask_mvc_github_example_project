"""
test api endpoints
"""
import uuid
import os
import pytest

from flaskr.settings import API_BASE_ENDPOINT
from flaskr.app import APP

TEST_RUNNER_ID = str(uuid.uuid4())
TEST_BRANCH_NAME = 'requests_test_{}'.format(TEST_RUNNER_ID)
TEST_FILE_NAME = 'test_file_99d4c5aa-4a57-4e76-9962-e38ea5a54895.txt'


@pytest.mark.parametrize(
    "test_name, "
    "method, "
    "endpoint, "
    "params, "
    "expected_success_status_code", [

        ('create branch',
         'post',
         '{}/branches'.format(API_BASE_ENDPOINT),
         {'branch_name_tgt': TEST_BRANCH_NAME, 'branch_name_src': 'master'},
         201),

        ('get branches',
         'get',
         '{}/branches'.format(API_BASE_ENDPOINT),
         None,
         200),

        ('create file upload',
         'post',
         '{}/branches/{}/files'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME),
         {'commit_message': 'pytest'},
         201),

        ('edit file',
         'put',
         '{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME),
         {'commit_message': 'pytest'},
         200),

        ('delete file',
         'delete',
         '{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME),
         {'commit_message': 'pytest'},
         200),

        ('create file form',
         'post',
         '{}/branches/{}/files'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME),
         {'commit_message': 'pytest', 'file_name': TEST_FILE_NAME},
         201),

        ('override file',
         'put',
         '{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME),
         {'commit_message': 'pytest'},
         200),

        ('get files',
         'get',
         '{}/branches/{}/files'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME),
         None,
         200),

        ('delete file',
         'delete',
         '{}/branches/{}/files/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME, TEST_FILE_NAME),
         {'commit_message': 'pytest'},
         200),

        ('delete branch',
         'delete',
         '{}/branches/{}'.format(API_BASE_ENDPOINT, TEST_BRANCH_NAME),
         None,
         200),
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
        response = APP.test_client().get(endpoint)

    elif method == "post":
        if test_name == "create branch":
            response = APP.test_client().post(endpoint,
                                              data=params)

        elif test_name == "create file upload":
            with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
                data = params
                data['uploaded_file'] = (fp, fp.name)
                response = APP.test_client().post(endpoint,
                                                  content_type="multipart/form-data",
                                                  data=data)

        elif test_name == "create file form":
            with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
                file_content = fp.read()
                data = params
                data['file_contents'] = file_content
                response = APP.test_client().post(endpoint,
                                                  data=data)

        else:
            raise NotImplementedError

    elif method == "put":
        if test_name == "edit file":
            with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
                file_content = fp.read()
                data = params
                data['file_contents'] = file_content
                response = APP.test_client().put(endpoint,
                                                 data=data)

        elif test_name == "override file":
            with open(os.path.join(os.getcwd(), 'files', TEST_FILE_NAME), 'rb') as fp:
                data = params
                data['uploaded_file'] = (fp, fp.name)
                response = APP.test_client().put(endpoint,
                                                 content_type="multipart/form-data",
                                                 data=data)

        else:
            raise NotImplementedError

    elif method == "delete":
        response = APP.test_client().delete(endpoint,
                                            data=params)

    assert response.status_code == expected_success_status_code
