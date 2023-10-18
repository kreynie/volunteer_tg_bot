from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn

from src.database.exceptions import EntityNotFound, handle_database_error
from src.schemas.sort import QueryOrderBySchema


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    @handle_database_error
    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        try:
            res = await self.session.execute(stmt)
        except IntegrityError:
            raise
        return res.scalar_one()

    @handle_database_error
    async def edit_one(self, filter_by_id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=filter_by_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    @handle_database_error
    async def find_all(
            self,
            offset: int = 0,
            limit: int = 0,
            filter_by: dict | None = None,
            order_by: list[MappedColumn] | None = None,
    ):
        stmt = select(self.model)
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        if order_by:
            stmt = stmt.order_by(*order_by)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        res = res.all()
        if res:
            res = [row[0].to_read_model() for row in res]
        return res

    @handle_database_error
    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res is not None:
            res = res.to_read_model()
        return res

    @handle_database_error
    async def delete_one(self, **filter_by) -> int:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except NoResultFound:
            raise EntityNotFound

    def build_order(self, order_by: QueryOrderBySchema | list[QueryOrderBySchema]) -> list[MappedColumn]:
        if not isinstance(order_by, list):
            order_by = [order_by]

        new_order = []
        for sort_schema in order_by:
            column = getattr(self.model, sort_schema.column_name, None)
            if column:
                new_order.append(column.desc() if sort_schema.sort_desc else column.asc())
        return new_order
