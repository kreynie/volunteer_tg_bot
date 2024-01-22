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
    moderator_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=0)

    role: Mapped["Role"] = relationship()

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            telegram_id=self.telegram_id,
            moderator_id=self.moderator_id,
            username=self.username,
            role_id=self.role_id,
        )
