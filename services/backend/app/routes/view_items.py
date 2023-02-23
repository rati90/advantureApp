from fastapi import APIRouter, status, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.backend.app.db.session import get_db
from ..core.security import get_current_active_user
from ..schemas import ItemCreate, Item, User, Image
from ..db.crud.crud_item import get_item_by_title, create_item, get_items
from ..db.crud.crud_image import get_image_by_item, create_image

router_item = APIRouter(
    prefix="/items",
    tags=["ITEMS"],
    responses={404: {"description": "Not found"}},
)


@router_item.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=Item

)
async def create_new_item(
        item: ItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    db_item = await get_item_by_title(db=db, item_title=item.title)
    if db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with this {db_item.title} title Already created",
        )

    return await create_item(db=db, item=item, user_id=current_user.id)


@router_item.get("/all", response_model=list[Item])
async def read_items(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    items = await get_items(db=db, skip=skip, limit=limit)

    return items


@router_item.get("/{item_title}")
async def read_item(item_title: str, db: AsyncSession = Depends(get_db)):
    db_item = await get_item_by_title(db=db, item_title=item_title)

    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_item


@router_item.post(
    "/create/{item_id}/image", status_code=status.HTTP_201_CREATED, response_model=Image

)
async def create_image_item(item_title: str,
                            file: UploadFile = File(None),
                            db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_active_user)
                            ):
    db_item = await get_item_by_title(db=db, item_title=item_title)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with this {item_title} item already created",
        )


    db_image = await get_image_by_item(db=db, item_id=db_item.id)

    if db_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item om this {db_item.title} item already created",
        )

    file_name = file.filename
    extension = file_name.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return {"error": "Invalid image format. Only JPG, JPEG and PNG are allowed."}
    image = await file.read()
#
    #image = bytes(str(image), 'utf-8')
    return await create_image(db=db, file=image, file_name=file_name, item_id=db_item.id)
