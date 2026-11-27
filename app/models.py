from datetime import UTC, datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.schemas import PriorityEnum


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    priority: Mapped[PriorityEnum] = mapped_column(
        SQLEnum(PriorityEnum), default=PriorityEnum.NORMAL
    )
    due_date: Mapped[datetime | None] = mapped_column(DateTime, index=True, 
                                                      nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
