'''Root of all configuration (mostly from environment variables)'''

import logging
from typing import List, Union, Optional

from pydantic import AnyUrl, BaseSettings, PostgresDsn


class Settings(BaseSettings):
    cors_origins: List[str] = ['*']
    app_log_level: Union[int, str] = logging.INFO

class DBSettings(BaseSettings):
    # DB to connect to (from environment variable). Default is in-memory DB (content will be lost!)
    db_uri: Union[PostgresDsn, AnyUrl] = 'sqlite+aiosqlite:///:memory:'
    db_schema_map: Optional[List[str]] = None

    class Config:
        env_file = ".env"

class GenesisDBSettings(BaseSettings):
    genesis_db_uri:  AnyUrl 

    class Config:
        env_file = ".env"
