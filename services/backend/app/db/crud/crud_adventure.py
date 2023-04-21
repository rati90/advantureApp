from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from uuid import UUID
import uuid

from ...models import Adventure, AdventureGroup
from .base import CRUDBase
from ...schemas import AdventureCreate, AdventureUpdate


class CRUDAdventure(CRUDBase[Adventure, AdventureCreate, AdventureUpdate]):
    async def get_by_title(self,
                           db: AsyncSession,
                           *,
                           title: str) -> Adventure | None:
        query = select(Adventure).where(Adventure.title == title)
        result = await db.execute(query)
        return result.scalar_one_or_none()


    async def get_items(self, db: AsyncSession, adventure_id: UUID, skip: int = 0, limit: int = 100):
        query = select(AdventureGroup).where(AdventureGroup.adventure_id == adventure_id)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self,
                     db: AsyncSession,
                     adventure_in: AdventureCreate,
                     item_id: UUID,
                     user_id: UUID
                     ):

        adventure_id = uuid.uuid4()
        db_adventure = Adventure(
            id=adventure_id,
            title=adventure_in.title,
            description=adventure_in.description,
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


    async def add_item_adventure(self,
                                 db: AsyncSession,
                                 item_id: UUID,
                                 adventure_id: UUID
                                 ):

        db_group = AdventureGroup(
            item_id=item_id,
            adventure_id=adventure_id
        )
        db.add(db_group)
        await db.commit()
        await db.refresh(db_group)

        return {"message": "item added to the adventure"}


    async def remove_by_title(self, db: AsyncSession, title: str):
        query = delete(Adventure).where(Adventure.title == title)
        await db.execute(query)

        return {"message": "deleted"}


adventure = CRUDAdventure(Adventure)
