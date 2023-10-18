from src.schemas.shift import ShiftLogSchema, ToggleShiftSchema
from src.schemas.sort import QueryOrderBySchema
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

    async def get_shift_history(
            self,
            user_id: int = None,
            offset: int = 0,
            limit: int = 0,
            order_by: QueryOrderBySchema | list[QueryOrderBySchema] | None = None,
    ) -> list[ShiftLogSchema]:
        async with self.uow:
            if order_by:
                order_by = self.uow.shift_logs.build_order(order_by)

            history = await self.uow.shift_logs.find_all(
                offset=offset,
                limit=limit,
                filter_by={"user_id": user_id} if user_id else None,
                order_by=order_by,
            )
            return history
