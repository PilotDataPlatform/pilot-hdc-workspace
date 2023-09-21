# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from common import LoggerFactory
from fastapi import APIRouter
from fastapi.responses import Response
from fastapi_utils import cbv

logger = LoggerFactory('api_health').get_logger()

router = APIRouter(tags=['Health'])


@cbv.cbv(router)
class Health:
    @router.get(
        '/health/',
        summary='Health check',
    )
    async def get(self):
        logger.debug('Starting api_health checks for workspace service')
        return Response(status_code=204)
