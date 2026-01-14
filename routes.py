from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Item
from schemas import ItemResponseSchema, ItemCreateSchema, PurchaseCreateSchema, PurchaseResponseSchema, \
    UpdateRequestSchema

router = APIRouter()


@router.get("/items", response_model=list[ItemResponseSchema])
async def all_items(max_price: Optional[Decimal] = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Item)

    if max_price:
        stmt = stmt.where(Item.price <= max_price)

    result = await db.execute(stmt)
    items = result.scalars().all()
    return items

@router.post("/item/{item_id}", response_model=ItemResponseSchema, status_code=201)
async def add_item(item_id: int, data: ItemCreateSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Item).where(Item.id == item_id)
    )
    item = result.scalars().one_or_none()

    if item:
        raise HTTPException(status_code=409, detail=f"Item with {item_id} already exist with name {item.name}")

    new_item = Item(id=item_id, name=data.name, quantity=data.quantity, price=data.price)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@router.post("/items/{item_id}/buy", response_model=PurchaseResponseSchema)
def purchase_item(item_id: int, data: PurchaseCreateSchema, db: list = Depends(get_db)):
    item = next((item for item in db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=400, detail="Invalid Item Id")
    if item["quantity"] < 1:
        raise HTTPException(status_code=409, detail=f"Stock Out for {item['name']}")
    if data.amount_paid < item["price"]:
        raise HTTPException(status_code=400, detail="Item is more expensive then input amount")

    item["quantity"] -= 1

    return {"status": "success",
            "item": item["name"],
            "change": data.amount_paid - item["price"]}


@router.put("/item/{item_id}", response_model=ItemResponseSchema)
def update_item(item_id: int, data: UpdateRequestSchema, db: list = Depends(get_db)):
    item = next((item for item in db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=400, detail="Invalid Item Id!")
    item["quantity"] = data.quantity
    return item
