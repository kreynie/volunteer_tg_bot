from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.role import RoleSchema
from .base import Base


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(unique=True)
    rights: Mapped[int] = mapped_column(default=0)

    def to_read_model(self) -> RoleSchema:
        return RoleSchema(
            id=self.id,
            name=self.name,
            rights=self.rights,
        )
