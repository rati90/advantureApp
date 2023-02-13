from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status, HTTPException

from services.backend.app.models import User, Profile
from ...internal import auth
from ...schemas import UserInDB, ProfileCreate


async def get_user(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, id: int):
    query = select(User).where(User.id == id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(User)
    result = await db.execute(query)
    return result.scalars().all()


async def get_profile(db: AsyncSession, user_id: int):
    query = select(Profile).where(Profile.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserInDB):
    user.hashed_password = auth.get_password_hash(
        user.hashed_password
    )

    db_user = User(
        email=user.email,
        hashed_password=user.hashed_password,
        role=user.role,
        is_active=user.is_active,
    )

    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_update_profile(
    db: AsyncSession, user_id: int, update_info: dict[str, str]
):
    query = (
        update(Profile).where(Profile.user_id == user_id).values(update_info)
    )
    await db.execute(query)
    return {"message": "updated"}


async def create_profile(
    db: AsyncSession, profile: ProfileCreate, user_id: int
):
    db_profile = Profile(
        first_name=profile.first_name,
        last_name=profile.last_name,
        bio=profile.bio,
        user_id=user_id,
    )
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)

    return db_profile


async def user_is_admin(current_user: User):
    if current_user.role == 3:
        return True

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized person",
        )

