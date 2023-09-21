# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from pydantic import BaseModel
from pydantic import Field

from app.models.base import APIResponse


class GetConnection(BaseModel):
    container_code: str


class GetConnectionResponse(APIResponse):
    result: dict = Field({}, example={'id': '9', 'name': 'workspace_indoctestproject', 'protocol': 'ssh'})


class PostConnection(BaseModel):
    container_code: str
    connection_name: str = ''
    username: str
    port: int
    hostname: str


class DeleteConnection(BaseModel):
    container_code: str
    connection_name: str


class DeleteConnectionResponse(APIResponse):
    result: str = Field('', example='success')
