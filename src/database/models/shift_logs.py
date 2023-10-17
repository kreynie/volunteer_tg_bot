from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from src.schemas.shift import ShiftLogSchema

if TYPE_CHECKING:
    from .users import User


class ShiftLog(Base):
    __tablename__ = "shift_logs"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    shift_action_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"))
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship()

    def to_read_model(self) -> ShiftLogSchema:
        return ShiftLogSchema(
            id=self.id,
            user_id=self.user_id,
            shift_action_id=self.shift_action_id,
            time=self.time,
        )
