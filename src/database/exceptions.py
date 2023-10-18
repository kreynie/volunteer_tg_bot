from sqlalchemy.exc import DatabaseError


class RepositoryError(Exception):
    pass


class EntityNotFound(RepositoryError):
    pass


class EntityAlreadyExists(RepositoryError):
    pass


def handle_database_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DatabaseError as e:
            print(f"Database Error: {e}")

    return wrapper
