from datetime import datetime

from .base import BaseSchema


class ShiftSchema(BaseSchema):
    name: str


class ShiftLogSchema(BaseSchema):
    user_id: int
    shift_action_id: int
    time: datetime
