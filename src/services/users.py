from src.database.exceptions import EntityAlreadyExists
from src.schemas.user import UserDeleteSchema, UserGetSchema, UserSchema, UserAddSchema
from src.utils.unitofwork import IUnitOfWork


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserAddSchema) -> int:
        user_dict = user.model_dump()
        async with self.uow:
            should_return = self.uow.users.model.id
            returned_user_id = await self.uow.users.add_one(user_dict, should_return)
            await self.uow.commit()
            return returned_user_id

    async def delete_user(self, user: UserDeleteSchema) -> int:
        user_dict = user.model_dump(exclude_none=True)
        async with self.uow:
            should_return = self.uow.users.model.id
            returned_user_id = await self.uow.users.delete_one(returning=should_return, **user_dict)
            await self.uow.commit()
            return returned_user_id

    async def get_user(self, user: UserGetSchema) -> UserSchema | None:
        user_dict = user.model_dump(exclude_none=True)
        async with self.uow:
            found_user = await self.uow.users.find_one(**user_dict)
            return found_user

    async def get_users(self) -> list[UserSchema]:
        async with self.uow:
            user = await self.uow.users.find_all()
            return user

    async def check_rights(self, user_tg_id: int, required_rights: int) -> bool:
        async with self.uow:
            user = await self.get_user(UserGetSchema(telegram_id=user_tg_id))
            if user is None:
                return False
            role = await self.uow.roles.find_one(id=user.role_id)
            return role.rights >= required_rights
