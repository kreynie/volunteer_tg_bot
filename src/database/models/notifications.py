from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from src.schemas.notifications import NotificationSchema

if TYPE_CHECKING:
    from .users import User


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    notification_id: Mapped[int]
    enabled: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship()

    def to_read_model(self) -> NotificationSchema:
        return NotificationSchema(
            id=self.id,
            user_id=self.user_id,
            notification_id=self.notification_id,
            enabled=self.enabled,
        )
