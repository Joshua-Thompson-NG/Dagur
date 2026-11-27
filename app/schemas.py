from datetime import datetime
from enum import Enum, StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PriorityEnum(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=250)
    description: str | None = None
    priority: PriorityEnum = PriorityEnum.NORMAL
    due_date: datetime | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=250)
    description: str | None = None
    is_completed: bool | None = None
    priority: PriorityEnum | None = None
    due_date: datetime | None = None

class TaskPublic(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
