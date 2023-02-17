from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.backend.app.models import Image


async def get_image_by_item(db: AsyncSession, item_id: str):
    query = select(Image).where(Image.item_id == item_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_image(db: AsyncSession, image: Image):

    db_item = Image(
        name=image.name,
        file=image.file,
        item_id=image.item_id
    )
    db.add(db_item)

    await db.commit()
    await db.refresh(db_item)

    return db_item

