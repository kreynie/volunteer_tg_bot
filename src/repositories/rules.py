from src.database.models import Rules
from src.utils.repositories import SQLAlchemyRepository


class RulesRepository(SQLAlchemyRepository):
    model = Rules
