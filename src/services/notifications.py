from src.schemas import notifications as schemas
from src.utils.unitofwork import IUnitOfWork


class NotificationsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
        self.__rules_list: list[schemas.NotificationSchema] = list()

    async def enable_notification(self, notification: schemas.EnableNotificationSchema) -> str:
        notification = notification.model_dump()
        async with self.uow:
            notification_id = await self.uow.notifications.edit_one(
                data=notification,
                returning=self.uow.notifications.model.id
            )
            await self.uow.commit()
            return notification_id

    async def disable_notification(self, notification: schemas.DisableNotificationSchema) -> str:
        notification = notification.model_dump()
        async with self.uow:
            notification_id = await self.uow.notifications.edit_one(
                data=notification,
                returning=self.uow.notifications.model.id
            )
            await self.uow.commit()
            return notification_id

    async def get_notifications_for_user(self, user_id: int) -> list[schemas.NotificationSchema]:
        async with self.uow:
            rules = await self.uow.notifications.find_all(filter_by={"user_id": user_id})
            return rules
