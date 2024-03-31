from src.database.models import Notification
from src.utils.repositories import SQLAlchemyRepository


class NotificationsRepository(SQLAlchemyRepository):
    model = Notification
