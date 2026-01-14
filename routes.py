from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from database import get_db
from schemas import ItemResponseSchema, ItemCreateSchema, PurchaseCreateSchema, PurchaseResponseSchema, \
    UpdateRequestSchema

router = APIRouter()

@router.get("/items", response_model=list[ItemResponseSchema])
def all_items(max_price: Optional[float] = None, db: list = Depends(get_db)):
    if max_price is None:
        return db

    return [item for item in db if item["price"] <= max_price]

@router.post("/item/{item_id}", response_model=ItemResponseSchema, status_code=201)
def new_item(item_id: int, data: ItemCreateSchema, db: list = Depends(get_db)):
    for item in db:
        if item["id"] == item_id:
            raise HTTPException(status_code=409, detail="Item already exists")

    item = {
        "id": item_id,
        "name": data.name,
        "quantity": data.quantity,
        "price": data.price
    }
    db.append(item)
    return ItemResponseSchema(**item)

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

