import logging
from typing import Optional, List

from sqlalchemy.future import select

from app.models import Application
from app.schemas import ApplicationCreate
import app.logging_config
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

logger_debug = logging.getLogger('log_debug')
logger_error = logging.getLogger('log_error')

async def add_application_to_db(application: ApplicationCreate, db: AsyncSession) -> Application:
    """
    Adds a new application to the database and returns the created application.
    """
    try:
        validated_application = ApplicationCreate(**application.model_dump())
        new_application = Application(**validated_application.model_dump())
        db.add(new_application)
        await db.commit()
        await db.refresh(new_application)
        return new_application

    except ValidationError as e:
        logger_error.error(f"Invalid application data: {e.errors()}")
        raise ValueError(f"Invalid application data: {e.errors()}") from e
    except Exception as e:
        logger_error.error(f"An error occurred while adding the application: {str(e)}")
        raise RuntimeError(f"An error occurred while adding the application: {str(e)}") from e

async def fetch_applications(db: AsyncSession, user_name: Optional[str], page: int, size: int) -> List[Application]:
    query = select(Application)
    if user_name:
        query = query.filter(Application.user_name == user_name)

    query = query.offset((page - 1) * size).limit(size)

    async with db as session:
        result = await session.execute(query)
        return result.scalars().all()