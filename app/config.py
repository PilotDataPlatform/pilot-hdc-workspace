# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from functools import lru_cache
from typing import Any

from pydantic import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    version = '2.2.7'
    APP_NAME: str = 'workspace_service'
    HOST: str = '0.0.0.0'
    PORT: int = 5068

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = 'json'

    AUTH_SERVICE: str

    WORKSPACE_PREFIX: str = 'workspace'

    GUACAMOLE_HOSTNAME: str
    GUACAMOLE_USERNAME: str
    GUACAMOLE_PASSWORD: str
    GUACAMOLE_URL_PATH: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)
        self.AUTH_SERVICE = self.AUTH_SERVICE + '/v1/'


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
