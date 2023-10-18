from pydantic import BaseModel
from .base import BaseSchema


class UserSchema(BaseSchema):
    telegram_id: int
    username: str | None
    role_id: int


class UserAddSchema(BaseModel):
    telegram_id: int
    username: str | None


class UserEditSchema(BaseModel):
    telegram_id: int
    role_id: int


class UserGetSchema(BaseModel):
    telegram_id: int


UserDeleteSchema = UserGetSchema
