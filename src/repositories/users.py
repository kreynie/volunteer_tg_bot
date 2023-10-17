from src.database.models import User
from src.utils.repositories import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
