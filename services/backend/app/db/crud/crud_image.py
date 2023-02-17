from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from services.backend.app.models import Image


async def get_image_by_item(db: AsyncSession, item_id: UUID):
    query = select(Image).where(Image.item_id == item_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_image(db: AsyncSession, file: bytes, file_name: str, item_id: UUID):

    db_image = Image(
        name=file_name,
        file=file,
        item_id=item_id,

    )
    db.add(db_image)

    await db.commit()
    await db.refresh(db_image)

    return db_image

