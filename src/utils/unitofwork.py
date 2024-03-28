from abc import ABC, abstractmethod

from src.database.database import session_maker
from src import repositories


class IUnitOfWork(ABC):
    users: repositories.UsersRepository
    roles: repositories.RolesRepository
    rules: repositories.RulesRepository
    shifts: repositories.ShiftsRepository
    shift_logs: repositories.ShiftLogsRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    """UnitOfWork for managing repositories"""

    def __init__(self):
        self.session_factory = session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = repositories.UsersRepository(self.session)
        self.roles = repositories.RolesRepository(self.session)
        self.rules = repositories.RulesRepository(self.session)
        self.shifts = repositories.ShiftsRepository(self.session)
        self.shift_logs = repositories.ShiftLogsRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
