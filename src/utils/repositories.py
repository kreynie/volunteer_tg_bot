from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoReferenceError, NoResultFound

from src.database.exceptions import EntityAlreadyExists, EntityNotFound, handle_database_error


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
    async def find_all(self, offset: int = 0, limit: int = 0, filter_by: dict = None):
        stmt = select(self.model)
        if filter_by:
            stmt.filter_by(**filter_by)
        if offset:
            stmt.offset(offset)
        if limit:
            stmt.limit(limit)
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
