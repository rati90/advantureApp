from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.backend.app.models import Item

from  services.backend.app.schemas import ItemCreate


async def get_item_by_title(db: AsyncSession, title: str):
    query = select(Item).where(Item.title == title)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_item(db: AsyncSession, item: ItemCreate, user_id):

    db_item = Item(
        title=item.title,
        description=item.description,
        price=item.price,
        image_id=item.image_id,
        user_id=user_id
    )

    db.add(db_item)

    await db.commit()
    await db.refresh(db_item)

    return db_item
