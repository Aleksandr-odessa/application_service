from app.kafka.kafka_manager import kafka_manager
from app.models import Application


async def send_application_message(application: Application) -> None:
    message = {
        "id": application.id,
        "user_name": application.user_name,
        "description": application.description,
        "created_at": application.created_at.isoformat(),
    }
    await kafka_manager.send_message(message)