from unittest.mock import AsyncMock, MagicMock

import pytest

from app.database.crud import add_application_to_db, fetch_applications
from app.models import Application
from app.schemas import ApplicationCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


@pytest.mark.asyncio
async def test_add_application_to_db():
    mock_session = AsyncMock(spec=AsyncSession)

    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    new_application_data = ApplicationCreate(user_name="test_user", description="test description")

    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await add_application_to_db(new_application_data, mock_session)

    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)

    assert mock_session.add.call_count == 1
    assert isinstance(mock_session.add.call_args[0][0], Application)
    assert mock_session.add.call_args[0][0].user_name == new_application_data.user_name
    assert mock_session.add.call_args[0][0].description == new_application_data.description

    assert result.user_name == new_application_data.user_name
    assert result.description == new_application_data.description


@pytest.mark.asyncio
async def test_fetch_applications_no_user_name():
    # Создаем мок-сессию
    mock_session = AsyncMock(spec=AsyncSession)
    # Устанавливаем поведение для контекстного менеджера (async with)
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = ['app1', 'app2']

    mock_session.execute.return_value = mock_result

    applications = await fetch_applications(mock_session, None, 1, 10)

    mock_session.execute.assert_called_once()

    executed_query = mock_session.execute.call_args[0][0]

    expected_query = str(select(Application).offset(0).limit(10))  # Ожидаемая строка запроса
    assert str(executed_query) == expected_query

    assert applications == ['app1', 'app2']


@pytest.mark.asyncio
async def test_fetch_applications_with_user_name():
    # Создаем мок-сессию
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = ['app1']

    mock_session.execute.return_value = mock_result

    applications = await fetch_applications(mock_session, 'JohnDoe', 1, 10)

    mock_session.execute.assert_called_once()

    executed_query = mock_session.execute.call_args[0][0]

    expected_query = str(select(Application).filter(Application.user_name == 'JohnDoe').offset(0).limit(10))
    assert str(executed_query) == expected_query

    assert applications == ['app1']
