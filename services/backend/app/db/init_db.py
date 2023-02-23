import asyncio
import typer

from .session import engine
from .session import Base
from ..models import user, item, adventure


async def init_models():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(user.Base.metadata.create_all)
        await conn.run_sync(item.Base.metadata.create_all)
        await conn.run_sync(adventure.Base.metadata.create_all)


cli = typer.Typer()


@cli.command()
async def db_init_models():
    await asyncio.run(init_models())



