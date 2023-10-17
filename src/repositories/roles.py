from src.database.models import Role
from src.utils.repositories import SQLAlchemyRepository


class RolesRepository(SQLAlchemyRepository):
    model = Role
