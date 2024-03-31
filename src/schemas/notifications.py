from pydantic import BaseModel


class GetUsersWithNotificationSchema(BaseModel):
    notification_id: int
    enabled: bool


class CreateNotificationSchema(GetUsersWithNotificationSchema):
    user_id: int


class GetUserNotificationSchema(CreateNotificationSchema):
    enabled: bool | None = None


class NotificationSchema(CreateNotificationSchema):
    id: int


class ToggleNotificationSchema(CreateNotificationSchema):
    pass
