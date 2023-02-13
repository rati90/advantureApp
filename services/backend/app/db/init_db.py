import asyncio
import typer

from .session import engine
from .session import mapper_registry

async def init_models():
    async with engine.begin() as conn:
        #await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)


cli = typer.Typer()


@cli.command()
async def db_init_models():
    await asyncio.run(init_models())

