from src.database.models import Shift
from src.utils.repositories import SQLAlchemyRepository


class ShiftsRepository(SQLAlchemyRepository):
    model = Shift
