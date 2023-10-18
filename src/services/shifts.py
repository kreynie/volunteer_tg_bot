from src.schemas.shift import ShiftLogSchema, ToggleShiftSchema
from src.utils.unitofwork import IUnitOfWork


class ShiftsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def toggle_shift(self, shift: ToggleShiftSchema) -> int:
        shift = shift.model_dump(exclude_none=True)
        async with self.uow:
            shift_id = await self.uow.shift_logs.add_one(shift)
            await self.uow.commit()
            return shift_id

    async def get_shift_history(self, user_id: int = None, limit: int = 10) -> list[ShiftLogSchema]:
        async with self.uow:
            history = await self.uow.shift_logs.find_all(limit=limit, filter_by={"id": user_id})
            return history
