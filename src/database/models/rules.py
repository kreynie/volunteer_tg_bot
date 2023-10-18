from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from ...schemas.rules import RuleSchema


class Rules(Base):
    __tablename__ = 'rules'

    text: Mapped[str] = mapped_column()

    def to_read_model(self) -> RuleSchema:
        return RuleSchema(
            id=self.id,
            text=self.text,
        )
