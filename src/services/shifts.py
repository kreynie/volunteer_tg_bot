from src.schemas.shift import ShiftSchema, ShiftLogSchema
from src.utils.unitofwork import IUnitOfWork


class ShiftsService:
    async def get_shifts(self, uow: IUnitOfWork) -> list[ShiftSchema]:
        async with uow:
            users = await uow.shifts.find_all()
            return users

    async def get_shift_history(self, uow: IUnitOfWork) -> list[ShiftLogSchema]:
        async with uow:
            history = await uow.shift_logs.find_all()
            return history
