from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db import init_db
from app.kafka.kafka_manager import kafka_manager
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the startup and shutdown of the application services.
    """
    await init_db()
    await kafka_manager.startup()
    yield
    await kafka_manager.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
