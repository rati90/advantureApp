from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from uuid import UUID

from .base import CRUDBase
from ...models import Item

from ...schemas import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def get_by_title(self,
                           db: AsyncSession,
                           *,
                           title: str) -> Item | None:
        query = select(Item).where(Item.title == title)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def remove_by_title(self,
                              db: AsyncSession,
                              title: str):
        query = delete(Item).where(Item.title == title)
        await db.execute(query)

        return {"message": "deleted"}

    async def create(self,
                     user_id: UUID,
                     db: AsyncSession,
                     *,
                     obj_in: ItemCreate) -> Item:
        db_obj = Item(
            title=obj_in.title,
            description=obj_in.description,
            price=obj_in.price,
            user_id=user_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


item = CRUDItem(Item)

