from src.schemas.shift import ShiftLogSchema, ShiftSchema, ToggleShiftSchema
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
            if not order_by:
                order_by = QueryOrderBySchema(column_name="id", sort_desc=True)
            order_by = self.uow.shift_logs.build_order(order_by)

            shift_logs: list[ShiftLogSchema] = await self.uow.shift_logs.find_all(
                offset=offset,
                limit=limit,
                filter_by={"user_id": user_id} if user_id else None,
                order_by=order_by,
            )
            if not shift_logs:
                return []
            shift_names = await self.get_shift_names()

            return self.__transform_shift_logs(shift_logs, shift_names)

    async def get_shift_names(self):
        shifts = await self.uow.shifts.find_all()
        return {shift.id: shift.name for shift in shifts}

    @staticmethod
    def __transform_shift_logs(self, shift_logs, shift_names):
        transformed_logs = []
        for log in shift_logs:
            transformed_log = ShiftLogSchema(
                shift_action_name=shift_names[log.shift_action_id],
                **log.model_dump(exclude_none=True),
            )
            transformed_logs.append(transformed_log)
        return transformed_logs
