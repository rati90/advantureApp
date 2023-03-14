from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.backend.app.core.security import get_current_active_user
from ..db.crud.crud_adventure import adventure

from ..db.crud.crud_item import item
from services.backend.app.db.session import get_db
from services.backend.app.schemas import Adventure, AdventureCreate, User

router_adventure = APIRouter(
    prefix="/adventure",
    tags=["ADVENTURES"],
    responses={404: {"description": "Not found"}},
)


@router_adventure.get("/all", response_model=list[Adventure])
async def read_adventures(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    adventures = await adventure.get_multi(db=db, skip=skip, limit=limit)

    return adventures


@router_adventure.get("/{adventure_title}/items")
async def read_adventure_items(adventure_title: str, db: AsyncSession = Depends(get_db)):
    db_adventure = await adventure.get_by_title(db=db, title=adventure_title)
    if db_adventure is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    adventure_items = await adventure.get_items(db=db, adventure_id=db_adventure.id)

    return adventure_items


@router_adventure.post("/create", status_code=status.HTTP_201_CREATED, response_model=Adventure)
async def create_new_adventure(
        adventure_in: AdventureCreate,
        item_title: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    db_adventure = await adventure.get_by_title(db=db, title=adventure_in.title)
    if db_adventure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Adventure with this {db_adventure.title} title Already created",
        )

    db_item = await item.get_by_title(db=db, title=item_title)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with {item_title} title does not exists",
        )

    return await adventure.create(db=db,
                                  adventure_in=adventure_in,
                                  item_id=db_item.id,
                                  user_id=current_user.id
                                  )


@router_adventure.post("/add_item", status_code=status.HTTP_201_CREATED)
async def add_new_item(
        adventure_title: str,
        item_title: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    db_adventure = await adventure.get_by_title(db=db, title=adventure_title)
    if db_adventure and db_adventure.user_id == current_user.id:
        db_item = await item.get_by_title(db=db, title=item_title)
        if db_item:
            return await adventure.add_item_adventure(db=db, item_id=db_item.id, adventure_id=db_adventure.id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item with this {item_title} title does not exists",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Adventure with this {adventure_title} title does not exists",
        )


@router_adventure.delete("/{adventure_title}")
async def delete_adventure(adventure_title: str,
                           db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    db_adventure = await adventure.get_by_title(db=db, title=adventure_title)
    if db_adventure and db_adventure.user_id == current_user.id:
        return await adventure.remove_by_title(db=db, title=adventure_title)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router_adventure.get("/{adventure_title}")
async def read_adventure(adventure_title: str, db: AsyncSession = Depends(get_db)):
    db_adventure = await adventure.get_by_title(db=db, title=adventure_title)

    if db_adventure is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_adventure
