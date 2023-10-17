from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.user import UserSchema
from .base import Base

if TYPE_CHECKING:
    from .roles import Role


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)

    role: Mapped["Role"] = relationship()

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            telegram_id=self.telegram_id,
            role_id=self.role_id,
        )
