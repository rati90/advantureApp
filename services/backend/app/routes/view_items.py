from fastapi import APIRouter, status, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.backend.app.db.session import get_db
from services.backend.app.schemas import Item, Image
from ..db.crud.crud_item import get_item_by_title, create_item
from ..db.crud.crud_image import create_image


route_item = APIRouter(
    prefix="/items",
    tags=["ITEMS"],
    responses={404: {"description": "Not found"}},
)


@route_item.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=Item

)
async def create_new_item(
        item: Item, image: Image, file: UploadFile, db: AsyncSession = Depends(get_db)
):

    db_item = await get_item_by_title(db=db, title=item.title)
    if db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with this {db_item.title} title Already created",
        )

    if image is not None:

        image.file = file
        await create_image(db=db, image=image)

    item.image = image

    return create_item(db=db, item=item)


