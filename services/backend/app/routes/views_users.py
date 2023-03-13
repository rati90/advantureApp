from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import get_current_active_user
from ..db.session  import get_db
from ..schemas import User, UserInDB, ProfileCreate, Profile, UserCreate

from ..db.crud.crud_user import (
    get_users,
    get_user,
    create_user,
    get_user_by_email,
    get_profile,
    create_profile,
    get_update_profile,
    user_is_admin,
)


router = APIRouter(
    prefix="/users",
    tags=["USERS"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=User
)
async def create_new_user(user_in: UserCreate,
                          db: AsyncSession = Depends(get_db),
                          ):
    db_user = await get_user_by_email(db=db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this {db_user.email} email Already created",
        )

    return await create_user(db=db, user=user_in)


@router.get("/all", response_model=list[User])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    if await user_is_admin(current_user):
        users = await get_users(db=db, skip=skip, limit=limit)
        return users


@router.get("/profile")
async def read_user_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_profile = await get_profile(db=db, user_id=current_user.id)
    if db_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_profile


@router.post("/profile/create", response_model=Profile)
async def create_new_profile(
    profile: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_profile = await get_profile(db=db, user_id=current_user.id)
    if db_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Profile already exists",
        )

    return await create_profile(
        db=db, profile=profile, user_id=current_user.id
    )


@router.patch("/profile")
async def update_profile(
    update_info: dict[str, str],
    db: AsyncSession = Depends(
        get_db,
    ),
    current_user: User = Depends(get_current_active_user),
):

    db_profile = await get_profile(db=db, user_id=current_user.id)
    if db_profile:
        return await get_update_profile(
            db=db, user_id=current_user.id, update_info=update_info
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_user


