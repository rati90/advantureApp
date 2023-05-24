from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from uuid import UUID

from .base import CRUDBase
from ...models import Category

from ...schemas import CategoryCreate, CategoryUpdate


class CRUDItem(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_name(self,
                          db: AsyncSession,
                          *,
                          name: str) -> Category | None:
        query = select(Category).where(Category.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(self,
                     db: AsyncSession,
                     *,
                     obj_in: CategoryCreate) -> Category:
        db_obj = Category(
            name=obj_in.name,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


category = CRUDItem(Category)
