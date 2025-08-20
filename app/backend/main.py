#!/usr/bin/python3
"""Main module for the API"""

from fastapi import FastAPI
from api.v1 import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="My API")

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
