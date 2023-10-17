from abc import ABC
from pydantic import BaseModel


class BaseSchema(BaseModel, ABC):
    id: int

    class Config:
        from_attributes = True
