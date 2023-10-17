from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.shift import ShiftSchema
from .base import Base


class Shift(Base):
    __tablename__ = "shifts"

    name: Mapped[str] = mapped_column(unique=True)

    def to_read_model(self) -> ShiftSchema:
        return ShiftSchema(
            id=self.id,
            name=self.name,
        )
