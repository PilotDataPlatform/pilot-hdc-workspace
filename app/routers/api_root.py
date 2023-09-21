# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter

from app.config import ConfigClass

router = APIRouter()


@router.get('/')
async def get():
    """For testing if service's up."""
    return {'message': 'Service Workspace, Version: ' + ConfigClass.version}
