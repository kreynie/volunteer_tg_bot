from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.exceptions import EntityNotFoundError, handle_database_error


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    @handle_database_error
    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    @handle_database_error
    async def edit_one(self, filter_by_id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=filter_by_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    @handle_database_error
    async def find_all(self, offset: int = 0, limit: int = 0):
        stmt = select(self.model)
        if offset:
            stmt.offset(offset)
        if limit:
            stmt.limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    @handle_database_error
    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        result = res.scalar_one()
        if result:
            return result.to_read_model()
        else:
            raise EntityNotFoundError("Entity not found")

    @handle_database_error
    async def delete_one(self, filter_by_id: int) -> int:
        stmt = delete(self.model).filter_by(id=filter_by_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
