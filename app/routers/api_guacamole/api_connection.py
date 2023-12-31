# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from common import LoggerFactory
from fastapi import APIRouter
from fastapi import Depends
from fastapi_utils.cbv import cbv
from requests.exceptions import HTTPError

from app.commons.guacamole_client import get_guacamole_client
from app.config import ConfigClass
from app.models.base import APIResponse
from app.models.models_connection import DeleteConnection
from app.models.models_connection import DeleteConnectionResponse
from app.models.models_connection import GetConnection
from app.models.models_connection import GetConnectionResponse
from app.models.models_connection import PostConnection
from app.resources.error_handler import APIException

router = APIRouter()
API_TAG = 'Connection'


@cbv(router)
class Connection:
    logger = LoggerFactory(
        'api_guacamole',
        level_default=ConfigClass.LOG_LEVEL_DEFAULT,
        level_file=ConfigClass.LOG_LEVEL_FILE,
        level_stdout=ConfigClass.LOG_LEVEL_STDOUT,
        level_stderr=ConfigClass.LOG_LEVEL_STDERR,
    ).get_logger()

    @router.get(
        '/guacamole/connection',
        summary='Get connections for a project',
        tags=[API_TAG],
        response_model=GetConnectionResponse,
    )
    def get(self, data: GetConnection = Depends(GetConnection)):
        guacamole_client = get_guacamole_client(data.container_code)
        connections = guacamole_client.get_connections()
        result_containers = []
        for connection in connections['childConnections']:
            result_containers.append(
                {
                    'id': connection['identifier'],
                    'name': connection['name'],
                    'protocol': connection['protocol'],
                }
            )
        api_response = GetConnectionResponse()
        api_response.result = result_containers
        return api_response.json_response()

    @router.post('/guacamole/connection', summary='Add a new connection', tags=[API_TAG])
    def post(self, data: PostConnection):
        guacamole_client = get_guacamole_client(data.container_code)
        payload = {
            'name': data.connection_name,
            'parentIdentifier': 'ROOT',
            'protocol': 'ssh',
            'parameters': {
                'port': data.port,
                'hostname': data.hostname,
            },
            'attributes': {},
        }
        try:
            result = guacamole_client.add_connection(payload)
        except HTTPError as e:
            self.logger.error(f'Error adding guacamole connection: {e}')
            raise APIException(
                status_code=e.response.status_code, error_msg=f'Error adding guacamole connection: {e.response.json()}'
            )
        response = APIResponse()
        response.result = result
        return response.json_response()

    @router.delete(
        '/guacamole/connection',
        summary='Get a connection by container_code',
        tags=[API_TAG],
        response_model=DeleteConnectionResponse,
    )
    def delete(self, data: DeleteConnection = Depends(DeleteConnection)):
        guacamole_client = get_guacamole_client(data.container_code)
        connection = guacamole_client.get_connection_by_name(data.connection_name)
        try:
            guacamole_client.delete_connection(connection['identifier'])
        except HTTPError as e:
            self.logger.error(f'Erroring deleting guacamole connection: {e}')
            raise APIException(
                status_code=e.response.status_code, error_msg='Error deleting guacamole connection: {e.response.json()}'
            )
        api_response = APIResponse()
        api_response.result = 'success'
        return api_response.json_response()
