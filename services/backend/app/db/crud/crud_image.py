from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from .base import CRUDBase
from ...models import Image

from ...schemas import ImageCreate, ImageUpdate


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    async def get_image_by_item(self,
                                db: AsyncSession,
                                *,
                                item_id: UUID):
        query = select(Image).where(Image.item_id == item_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()


    async def create(self,
                     db: AsyncSession,
                     file: bytes,
                     file_name: str,
                     item_id: UUID,) -> Image:


        db_obj = Image(
                name=file_name,
                file=file,
                item_id=item_id,
            )
        db.add(db_obj)

        await db.commit()
        await db.refresh(db_obj)

        return db_obj


image = CRUDImage(Image)