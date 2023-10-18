from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__tablename__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
