from sqlalchemy import and_, ColumnElement, delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn

from src.database.exceptions import EntityAlreadyExists, EntityNotFound, handle_database_error
from src.schemas.sort import QueryOrderBySchema


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    @handle_database_error
    async def add_one(self, data: dict, returning: MappedColumn | None = None):
        stmt = insert(self.model).values(**data)
        if returning:
            stmt = stmt.returning(returning)
        try:
            res = await self.session.execute(stmt)
        except IntegrityError:
            raise EntityAlreadyExists
        return res.scalar_one()

    @handle_database_error
    async def edit_one(
            self,
            data: dict,
            filter_by: dict,
            returning: MappedColumn | None = None,
    ):
        stmt = update(self.model).values(**data)
        if filter_by:
            filter_by = self.build_filter(**filter_by)
            stmt = stmt.where(filter_by)
        if returning:
            stmt = stmt.returning(returning)
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except NoResultFound:
            raise EntityNotFound

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
            filter_by = self.build_filter(**filter_by)
            stmt = stmt.where(filter_by)
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
        filter_by = self.build_filter(**filter_by)

        stmt = select(self.model).where(filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res is not None:
            res = res.to_read_model()
        return res

    @handle_database_error
    async def delete_one(
            self,
            returning: MappedColumn | None = None,
            **filter_by,
    ):
        filter_by = self.build_filter(**filter_by)

        stmt = delete(self.model).where(filter_by)
        if returning is not None:
            stmt = stmt.returning(returning)
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

    def build_filter(self, **kwargs) -> ColumnElement[bool]:
        filter_clauses = []

        operators = {
            "__ne": lambda col, val: col != val,
            "__lt": lambda col, val: col < val,
            "__gt": lambda col, val: col > val,
            "__lte": lambda col, val: col <= val,
            "__gte": lambda col, val: col >= val,
            "__in": lambda col, val: col.in_(val),
            "__not_in": lambda col, val: col.not_in(val),
            "__like": lambda col, val: col.like(val),
        }

        for key, value in kwargs.items():
            for op, op_func in operators.items():
                if op in key:
                    column_name = key.replace(op, "")
                    filter_clauses.append(op_func(getattr(self.model, column_name), value))
                    break
            else:
                filter_clauses.append(getattr(self.model, key) == value)

        return and_(*filter_clauses)
