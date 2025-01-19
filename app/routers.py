from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import add_application_to_db, fetch_applications
from app.database.db import get_db_session
from app.kafka.kafka_producer import send_application_message
from app.schemas import ApplicationCreate, ApplicationResponse

router = APIRouter()

@router.post("/applications", response_model=ApplicationResponse, status_code=201)
async def create_application(
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new application.

    Parameters:
    - application (ApplicationCreate): The application data to be created.
    - db (AsyncSession): The database session dependency.
    """

    async with db as session:
        new_application = await add_application_to_db(application, session)
        await send_application_message(new_application)
    return new_application


@router.get("/applications", response_model=List[ApplicationResponse])
async def get_applications(
    user_name: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1),
    db: AsyncSession = Depends(get_db_session),
):
    """
        Retrieve a list of applications.
    """
    applications = await fetch_applications(db, user_name, page, size)
    return applications
