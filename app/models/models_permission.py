# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from app.models.base import APIResponse
from app.models.base import EAPIResponseCode
from app.resources.error_handler import APIException


class GetPermission(BaseModel):
    container_code: str
    username: str


class GetPermissionResponse(APIResponse):
    result: dict = Field({}, example={})


class PostPermission(BaseModel):
    connection_name: str
    container_code: str
    username: str
    permissions: list[str]
    operation: str

    @validator('operation')
    def validate_operation(cls, v):
        if v not in ['add', 'remove']:
            raise APIException(error_msg='Invalid operation', status_code=EAPIResponseCode.bad_request)
        return v


class CreateUser(BaseModel):
    container_code: str
    username: str


class CreateUserResponse(APIResponse):
    result: dict = Field('', example='success')


class CreateUserBulk(BaseModel):
    container_code: str


class CreateUserBulkResponse(APIResponse):
    result: dict = Field('', example='success')
