from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Item

async def seed_items(db: AsyncSession):
    result = await db.execute(select(Item))
    existing_items = result.scalars().first()

    if existing_items:
        return

    items = [
        Item(name="Water Bottle", quantity=25, price=Decimal("20.00")),
        Item(name="Chips", quantity=15, price=Decimal("30.00")),
        Item(name="Chocolate Bar", quantity=1, price=Decimal("40.00")),
        Item(name="Soft Drink", quantity=18, price=Decimal("35.00")),
        Item(name="Cookies", quantity=12, price=Decimal("25.00")),
    ]

    db.add_all(items)
    await db.commit()