from src.schemas import notifications as schemas
from src.utils.unitofwork import IUnitOfWork


class NotificationsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
        self.__rules_list: list[schemas.NotificationSchema] = list()

    async def create_notification(self, notification: schemas.CreateNotificationSchema) -> int:
        notification = notification.model_dump()
        async with self.uow:
            notification_id = await self.uow.notifications.add_one(
                data=notification,
                returning=self.uow.notifications.model.id
            )
            await self.uow.commit()
            return notification_id

    async def toggle_notification(self, notification: schemas.ToggleNotificationSchema) -> int:
        notification_dict = notification.model_dump()
        filter_by = notification_dict.copy()
        del filter_by["enabled"]
        async with self.uow:
            notification_id = await self.uow.notifications.edit_one(
                data=notification_dict,
                filter_by=filter_by,
                returning=self.uow.notifications.model.id
            )
            await self.uow.commit()
            return notification_id

    async def get_user_notification(
            self,
            notification: schemas.GetUserNotificationSchema,
    ) -> schemas.NotificationSchema | None:
        filter_by = notification.model_dump(exclude_none=True)

        async with self.uow:
            returned_notification = await self.uow.notifications.find_one(**filter_by)
            return returned_notification

    async def get_users_with_notification(
            self,
            notification: schemas.GetUsersWithNotificationSchema,
    ) -> list[schemas.NotificationSchema]:
        filter_by = notification.model_dump()

        async with self.uow:
            returned_records = await self.uow.notifications.find_all(filter_by=filter_by)
            return returned_records
