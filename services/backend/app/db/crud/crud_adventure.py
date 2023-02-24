from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from uuid import UUID
import uuid
from services.backend.app.models import Adventure, AdventureGroup

from services.backend.app.schemas import AdventureCreate


async def get_adventure_by_title(db: AsyncSession, adventure_title: str):
    query = select(Adventure).where(Adventure.title == adventure_title)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_adventures(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Adventure)
    result = await db.execute(query)
    return result.scalars().all()


async def get_delete_adventure(db: AsyncSession, adventure_title: str):
    query = delete(Adventure).where(Adventure.title == adventure_title)
    await db.execute(query)

    return {"message": "deleted"}


async def create_adventure(db: AsyncSession,
                           adventure: AdventureCreate,
                           item_id: UUID,
                           user_id: UUID,
                           ):

    adventure_id = uuid.uuid4()
    db_adventure = Adventure(
        id=adventure_id,
        title=adventure.title,
        description=adventure.description,
        user_id=user_id,
    )

    db.add(db_adventure)

    await db.commit()
    await db.refresh(db_adventure)

    db_group = AdventureGroup(
        item_id=item_id,
        adventure_id=adventure_id
    )
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)

    return db_adventure


async def add_item_adventure(
        db: AsyncSession,
        item_id=UUID,
        adventure_id=UUID

):
    db_group = AdventureGroup(
        item_id=item_id,
        adventure_id=adventure_id
    )
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)

    return {"message": "item added to the adventure"}
