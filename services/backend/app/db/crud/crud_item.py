from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from services.backend.app.models import Item

from  services.backend.app.schemas import ItemCreate


async def get_item_by_title(db: AsyncSession, item_title: str):
    query = select(Item).where(Item.title == item_title)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Item)
    result = await db.execute(query)
    return result.scalars().all()


async def create_item(db: AsyncSession,
                      item: ItemCreate,
                      user_id: UUID,
                      ):

    db_item = Item(
        title=item.title,
        description=item.description,
        price=item.price,
        user_id=user_id,

    )

    db.add(db_item)

    await db.commit()
    await db.refresh(db_item)

    return db_item
