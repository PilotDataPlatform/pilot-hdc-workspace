# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import FastAPI

from .routers import api_root
from .routers.api_guacamole import api_connection
from .routers.api_guacamole import api_permission
from .routers.api_health import api_health


def api_registry(app: FastAPI):
    app.include_router(api_health.router, prefix='/v1')
    app.include_router(api_root.router, prefix='/v1')
    app.include_router(api_connection.router, prefix='/v1')
    app.include_router(api_permission.router, prefix='/v1')
