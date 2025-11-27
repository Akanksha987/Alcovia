from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .database import Base, engine
from .routes import contents, users


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001 - FastAPI requires signature
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.include_router(users.router)
app.include_router(contents.router)


@app.get("/healthz", tags=["ops"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

