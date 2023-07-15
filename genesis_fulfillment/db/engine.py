
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncTransaction,
    AsyncConnection,
    AsyncEngine
)

from sqlalchemy.orm import sessionmaker

from genesis_fulfillment.config import GenesisDBSettings

from functools import lru_cache

from typing import Optional, Dict


Session = AsyncSession
Transaction = AsyncTransaction
Connection = AsyncConnection



######GENESIS
@lru_cache()
def get_engine() -> AsyncEngine:
    '''Create and return a db engine using the config'''
    db_settings = GenesisDBSettings()
    return create_async_engine(
        db_settings.genesis_db_uri,
        pool_size=20,
        pool_recycle=3600
    )


@lru_cache()
def get_sessionmaker():
    '''Return a sessionmaker object that uses the above engine'''
    engine = get_engine()
    return sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        future=True
    )

