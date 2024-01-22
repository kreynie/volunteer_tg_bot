from pydantic import BaseModel
from .base import BaseSchema


class UserSchema(BaseSchema):
    telegram_id: int
    moderator_id: int
    username: str | None
    role_id: int


class UserAddSchema(BaseModel):
    telegram_id: int
    moderator_id: int
    username: str | None


class UserUpdateSchema(BaseModel):
    id: int
    moderator_id: int
    role_id: int


class UserUpdatePartialSchema(BaseModel):
    id: int
    moderator_id: int | None = None
    role_id: int | None = None


class UserGetSchema(BaseModel):
    telegram_id: int


UserDeleteSchema = UserGetSchema
