from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.backend.app.routes.views_users import router
from .db.table_setup import cli, init_models


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    @cli.command()
    async def db_init_models():
        await init_models()


    return app


