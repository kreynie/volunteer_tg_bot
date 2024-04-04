from datetime import datetime

from pydantic import BaseModel

from .base import BaseSchema


class ShiftSchema(BaseSchema):
    name: str


class ToggleShiftSchema(BaseModel):
    user_id: int
    shift_action_id: int
    shift_action_name: str | None = None
    time: datetime | None


class ShiftLogSchema(BaseSchema, ToggleShiftSchema):
    moderator_id: int
