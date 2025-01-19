from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database.db import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.today(), nullable=False)
