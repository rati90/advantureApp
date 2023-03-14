from .base import CRUDBase

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from services.backend.app.models import Profile
from ...schemas import ProfileCreate, ProfileUpdate


class CRUDProfile(CRUDBase[Profile, ProfileCreate, ProfileUpdate]):
    async def get_by_user(self, db: AsyncSession, *, user_id: UUID) -> Profile | None:
        query = select(Profile).where(Profile.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(self,
                     db: AsyncSession,
                     user_id,
                     *,
                     obj_in: ProfileCreate) -> Profile:
        db_obj = Profile(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            bio=obj_in.bio,
            user_id=user_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # async def update(self,
    #                  db: AsyncSession,
    #                  user_id: UUID,
    #                  profile_update: ProfileUpdate
    # ):
    #     query = (
    #         update(Profile).where(Profile.user_id == user_id).values(profile_update)
    #     )
    #     await db.execute(query)
    #     return {"message": "updated"}


profile = CRUDProfile(Profile)


