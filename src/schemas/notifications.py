from .base import BaseSchema


class NotificationSchema(BaseSchema):
    id: int
    user_id: int
    notification_id: int
    enabled: bool


class ToggleNotificationSchema(BaseSchema):
    id: int


class EnableNotificationSchema(ToggleNotificationSchema):
    enabled: bool = True


class DisableNotificationSchema(ToggleNotificationSchema):
    enabled: bool = False
