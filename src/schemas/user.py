from pydantic import BaseModel
from .base import BaseSchema


class UserSchema(BaseSchema):
    telegram_id: int
    role_id: int


class UserSchemaAdd(BaseModel):
    telegram_id: int


class UserSchemaEdit(BaseModel):
    telegram_id: int
    role_id: int
