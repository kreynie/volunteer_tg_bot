from sqlalchemy import Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.rules import RuleSchema
from .base import Base


class Rules(Base):
    __tablename__ = 'rules'

    rule_number: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column(Text)

    __table_args__ = (UniqueConstraint("rule_number", name="rule_number"),)

    def to_read_model(self) -> RuleSchema:
        return RuleSchema(
            id=self.id,
            rule_number=self.rule_number,
            text=self.text,
        )
