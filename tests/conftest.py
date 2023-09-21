# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest
from fastapi.testclient import TestClient
from requests.exceptions import HTTPError

from app.main import create_app

GUACAMOLE_CONNECTION = {'identifier': '3', 'name': 'lxd_test', 'parentIdentifier': 'ROOT', 'protocol': 'ssh'}

GUACAMOLE_PERMISSION = {
    'connectionPermissions': {
        '3': [
            'READ',
            'UPDATE',
            'DELETE',
        ],
    }
}


def guacapy_mock(  # noqa: C901
    mocker, response_code=204, connection_exception=False, init_exception=False, add_user_exception=False
):
    class MockResponse:
        def __init__(self, response_code=response_code):
            self.status_code = response_code

        def json(self):
            return {}

    class GuacapyClientMock:
        def __init__(self, *args, **kwargs):
            if init_exception:
                response = MockResponse(response_code=503)
                raise HTTPError('', 503, 'Testing', response=response)

        def get_connections(self, *args, **kwargs):
            return {'childConnections': [GUACAMOLE_CONNECTION]}

        def get_connection_by_name(self, *args, **kwargs):
            return GUACAMOLE_CONNECTION

        def add_connection(self, *args, **kwargs):
            if connection_exception:
                response = MockResponse(response_code=400)
                raise HTTPError('', 400, 'Testing', response=response)
            return GUACAMOLE_CONNECTION

        def get_permissions(self, *args, **kwargs):
            return GUACAMOLE_PERMISSION

        def grant_permission(self, *args, **kwargs):
            return MockResponse(response_code=response_code)

        def delete_connection(self, *args, **kwargs):
            if connection_exception:
                response = MockResponse(response_code=400)
                raise HTTPError('', 400, 'Testing', response=response)
            return MockResponse(response_code=response_code)

        def add_user(self, *args, **kwargs):
            if add_user_exception:
                response = MockResponse(response_code=400)
                raise HTTPError('', 400, 'Testing', response=response)
            return {}

    mocker.patch('app.commons.guacamole_client.Guacamole', GuacapyClientMock)


@pytest.fixture
def guacapy_client_mock_connection_except(mocker):
    guacapy_mock(mocker, connection_exception=True)


@pytest.fixture
def guacapy_client_mock_grant_permission_400(mocker):
    guacapy_mock(mocker, response_code=400)


@pytest.fixture
def guacapy_client_mock_no_connection(mocker):
    guacapy_mock(mocker, init_exception=True, response_code=503)


@pytest.fixture
def guacapy_client_mock_add_user_400(mocker):
    guacapy_mock(mocker, add_user_exception=True, response_code=503)


@pytest.fixture
def guacapy_client_mock(mocker):
    guacapy_mock(mocker)


@pytest.fixture
def test_client():
    app = create_app()
    client = TestClient(app)
    return client
