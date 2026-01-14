from decimal import Decimal

from pydantic import BaseModel, Field


class ItemResponseSchema(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

    class Config:
        from_attributes: True

class ItemCreateSchema(BaseModel):
    name: str
    quantity: int = Field(..., gt=0, le=100)
    price: Decimal = Field(..., gt=0)

class PurchaseResponseSchema(BaseModel):
    status: str
    item: str
    change: float

class PurchaseCreateSchema(BaseModel):
    amount_paid: float = Field(..., gt=0)

class UpdateRequestSchema(BaseModel):
    quantity: int = Field(..., gt=0)
