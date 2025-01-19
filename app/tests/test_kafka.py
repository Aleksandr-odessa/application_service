from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from app.kafka.kafka_producer import send_application_message
from app.models import Application


@pytest.mark.asyncio
async def test_send_application_message():
    # Мокаем глобальный объект kafka_manager
    with patch("app.kafka.kafka_producer.kafka_manager") as mock_kafka_manager:
        # Настраиваем mock send_message как асинхронный метод
        mock_kafka_manager.send_message = AsyncMock()

        # Создаём фиктивный объект Application
        application = Application(
            id=1,
            user_name="test_user",
            description="Test application",
            created_at=datetime.now()
        )

        await send_application_message(application)

        # Проверяем, что send_message был вызван с ожидаемыми данными
        expected_message = {
            "id": application.id,
            "user_name": application.user_name,
            "description": application.description,
            "created_at": application.created_at.isoformat(),
        }
        mock_kafka_manager.send_message.assert_called_once_with(expected_message)
