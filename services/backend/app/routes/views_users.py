from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..core.security import get_current_active_user
from ..db.session import get_db
from ..schemas import User, UserCreate, Profile, ProfileCreate, ProfileUpdate

from ..db.crud.crud_user import user
from ..db.crud.crud_profile import profile

router = APIRouter(
    prefix="/user",
    tags=["USERS"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=User
)
async def create_new_user(user_in: UserCreate,
                          db: AsyncSession = Depends(get_db),
                          ):
    db_user = await user.get_by_email(db=db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this {db_user.email} email Already created",
        )

    return await user.create(db=db, obj_in=user_in)


@router.get("/all", response_model=list[User])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    if await user.is_admin(current_user):
        users = await user.get_multi(db=db, skip=skip, limit=limit)
        return users


@router.get("/profile")
async def read_user_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_profile = await profile.get_by_user(db=db, user_id=current_user.id)
    if db_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_profile


@router.post("/profile/create", response_model=Profile)
async def create_new_profile(
    profile_in: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_profile = await profile.get_by_user(db=db, user_id=current_user.id)
    if db_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Profile already exists",
        )

    return await profile.create(
        db=db, obj_in=profile_in, user_id=current_user.id
    )


@router.patch("/profile")
async def update_profile(
    profile_in: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):

    db_profile = await profile.get_by_user(db=db, user_id=current_user.id)
    if db_profile:
        return await profile.update(
            db=db, db_obj=db_profile, obj_in=profile_in,
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{user_id}")
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    db_user = await user.get(db=db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_user


