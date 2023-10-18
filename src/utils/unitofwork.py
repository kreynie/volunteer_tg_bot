from abc import ABC, abstractmethod

from src.repositories import RolesRepository, ShiftLogsRepository, ShiftsRepository, UsersRepository
from src.database.database import session_maker
from src.repositories.rules import RulesRepository


class IUnitOfWork(ABC):
    users: UsersRepository
    roles: RolesRepository
    rules: RulesRepository
    shifts: ShiftsRepository
    shift_logs: ShiftLogsRepository

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


class UnitOfWork:
    def __init__(self):
        self.session_factory = session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.roles = RolesRepository(self.session)
        self.rules = RulesRepository(self.session)
        self.shifts = ShiftsRepository(self.session)
        self.shift_logs = ShiftLogsRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
