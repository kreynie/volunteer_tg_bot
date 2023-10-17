from src.database.models import ShiftLogSchema
from src.utils.repositories import SQLAlchemyRepository


class ShiftLogsRepository(SQLAlchemyRepository):
    model = ShiftLogSchema
