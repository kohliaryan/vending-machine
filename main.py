from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine, Base,AsyncSessionLocal
from routes import router
from seed_data import seed_items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_items(session)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root() -> str:
    return "Server is running!"

app.include_router(router=router)