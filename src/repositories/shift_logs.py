from src.database.models import ShiftLog
from src.utils.repositories import SQLAlchemyRepository


class ShiftLogsRepository(SQLAlchemyRepository):
    model = ShiftLog
