'''
Mock Genesis app to host APIs similar to the phAIdelta Genesis app.
It also integrates Abot SDK fulfillment API
'''

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Routers
from genesis_fulfillment import genesis

from abot_sdk import AbotFulfillmentAPI, FulfillmentRouter

from genesis_fulfillment.db import BASE, Connection, get_engine
from genesis_fulfillment.config import Settings


def create_app() -> FastAPI:
    ### Application instance ###
    app = FastAPI()
    settings = Settings()

    logging.basicConfig(
        level=settings.app_log_level
    )

    logger = logging.getLogger(__name__)

    ### Middleware ###

    # Enable cross-origin request, from any domain (*)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ### App events ###
    @app.on_event("startup")
    async def init_tables():
        import asyncio
        from sqlalchemy.schema import CreateSchema
        from multiprocessing import Lock

        engine = get_engine()
        conn: Connection

        mutex = Lock()

        # schema_mapping = get_schema_mapping()

        with mutex: # Prevent multiple workers conflicting with each other
            async with engine.begin() as conn:
                logger.info("Creating/updating DB schema (if needed)...")
                await asyncio.gather(*[
                    conn.execute(
                        CreateSchema(schema_name, if_not_exists=True)
                    )
                    for schema_name in BASE.metadata._schemas
                ])
                logger.info("Creating/updating tables (if needed)...")
                await conn.run_sync(BASE.metadata.create_all)

    ### Exception handlers ###

    @app.exception_handler(OSError)
    async def unhandled_oserror_exception_handler(request: Request, exc: OSError):
        logger.exception("Unhandled OSError while serving a request:", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"exception": 'OSError', "detail": str(exc)}
        )

    ### Routes ###

    # Add routes to the application
    app.include_router(genesis.router)

    # Abot fulfillment API
    abot_api = AbotFulfillmentAPI(
        FulfillmentRouter(service_name="genesis", router=genesis.router),
        app_class="genesis",
        friendly_name="Genesis UAT",
        description="Genesis UAT platform interface",
        version="1.0.0"
    )

    app.include_router(abot_api)

    return app
