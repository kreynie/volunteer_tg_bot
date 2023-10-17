from .base import BaseSchema


class RoleSchema(BaseSchema):
    name: str
    rights: int
