from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.backend.app.schemas import Item


async def get_item_by_title(db: AsyncSession, title: str):
    query = select(Item).where(Item.title == title)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_item(db: AsyncSession, item: Item):

    db_item = Item(**item.dict())
    db.add(db_item)

    await db.commit()
    await db.refresh(db_item)

    return db_item
