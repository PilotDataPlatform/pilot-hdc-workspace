# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from common import LoggerFactory
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from app.commons.auth_service import get_project_users
from app.commons.guacamole_client import add_users_bulk
from app.commons.guacamole_client import get_guacamole_client
from app.config import ConfigClass
from app.models.base import EAPIResponseCode
from app.models.models_permission import CreateUser
from app.models.models_permission import CreateUserBulk
from app.models.models_permission import CreateUserBulkResponse
from app.models.models_permission import CreateUserResponse
from app.models.models_permission import GetPermission
from app.models.models_permission import GetPermissionResponse
from app.models.models_permission import PostPermission
from app.resources.error_handler import APIException

router = APIRouter()
API_TAG = 'Permission'


@cbv(router)
class Permission:
    logger = LoggerFactory(
        'api_permission',
        level_default=ConfigClass.LOG_LEVEL_DEFAULT,
        level_file=ConfigClass.LOG_LEVEL_FILE,
        level_stdout=ConfigClass.LOG_LEVEL_STDOUT,
        level_stderr=ConfigClass.LOG_LEVEL_STDERR,
    ).get_logger()

    @router.get(
        '/guacamole/permission',
        summary='Get permissons on a connection for a user',
        tags=[API_TAG],
        response_model=GetPermissionResponse,
    )
    def get(self, data: GetPermission = Depends(GetPermission)):
        guacamole_client = get_guacamole_client(data.container_code)
        connections = guacamole_client.get_connections()
        permissions = guacamole_client.get_permissions(data.username)
        result = {}
        for connection in connections['childConnections']:
            result[connection['name']] = permissions['connectionPermissions'].get(connection['identifier'], [])
        api_response = GetPermissionResponse()
        api_response.result = {'container_code': data.container_code, 'permissions': result}
        return api_response.json_response()

    @router.post('/guacamole/permission', summary='Add permissions for a user on a connection', tags=[API_TAG])
    def post(self, data: PostPermission):
        guacamole_client = get_guacamole_client(data.container_code)
        connection = guacamole_client.get_connection_by_name(data.connection_name)
        connection_id = connection['identifier']
        payload = []
        for permission in data.permissions:
            payload.append(
                {
                    'op': data.operation,
                    'path': f'/connectionPermissions/{connection_id}',
                    'value': permission,
                }
            )
        response = guacamole_client.grant_permission(data.username, payload)
        if response.status_code != 204:
            self.logger.error(f'Erroring updating guacamole permissions: {response}')
            raise APIException(
                status_code=response.status_code, error_msg='Error updating guacamole permisisons: {response.json()}'
            )
        return JSONResponse('success')


@cbv(router)
class User:
    logger = LoggerFactory(
        'api_permission',
        level_default=ConfigClass.LOG_LEVEL_DEFAULT,
        level_file=ConfigClass.LOG_LEVEL_FILE,
        level_stdout=ConfigClass.LOG_LEVEL_STDOUT,
        level_stderr=ConfigClass.LOG_LEVEL_STDERR,
    ).get_logger()

    @router.post(
        '/guacamole/users',
        summary='Create a new user in guacamole',
        tags=[API_TAG],
        response_model=CreateUserResponse,
    )
    def post(self, data: CreateUser):
        guacamole_client = get_guacamole_client(data.container_code)
        payload = {
            'username': data.username,
            'attributes': {
                'access-window-end': None,
                'access-window-start': None,
                'disabled': None,
                'expired': None,
                'guac-email-address': None,
                'guac-full-name': None,
                'guac-organization': None,
                'guac-organizational-role': None,
                'timezone': None,
                'valid-from': None,
                'valid-until': None,
            },
        }
        try:
            guacamole_client.add_user(payload)
        except Exception as e:
            self.logger.error(f'Error adding user in guacamole: {e}')
            raise APIException(
                error_msg='User already exists in guacamole', status_code=EAPIResponseCode.bad_request.value
            )
        api_response = CreateUserResponse()
        api_response.result = 'success'
        return api_response.json_response()


@cbv(router)
class ProjectUsers:
    logger = LoggerFactory(
        'api_permission',
        level_default=ConfigClass.LOG_LEVEL_DEFAULT,
        level_file=ConfigClass.LOG_LEVEL_FILE,
        level_stdout=ConfigClass.LOG_LEVEL_STDOUT,
        level_stderr=ConfigClass.LOG_LEVEL_STDERR,
    ).get_logger()

    @router.post(
        '/guacamole/project/users',
        summary='Create a new user in guacamole',
        tags=[API_TAG],
        response_model=CreateUserBulkResponse,
    )
    async def post(self, data: CreateUserBulk, background_tasks: BackgroundTasks):
        users = await get_project_users(data.container_code)
        background_tasks.add_task(add_users_bulk, users, data.container_code)
        api_response = CreateUserResponse()
        api_response.result = 'success'
        return api_response.json_response()
