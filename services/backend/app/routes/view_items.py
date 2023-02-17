from fastapi import APIRouter, status, UploadFile, File, Depends, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from services.backend.app.db.session import get_db
from ..core.security import get_current_active_user
from ..schemas import ItemCreate, Image, Item, User
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
        item: ItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    #file: UploadFile
    db_item = await get_item_by_title(db=db, title=item.title)
    if db_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with this {db_item.title} title Already created",
        )
    # image = Image()
    # if image is not None:
    #
    #     image.file = file
    #     await create_image(db=db, image=image)

   # item.image = image

    return await create_item(db=db, item=item, user_id=current_user.id)


