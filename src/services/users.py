from src.schemas.user import UserSchema, UserSchemaAdd
from src.utils.unitofwork import IUnitOfWork


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserSchemaAdd):
        user_dict = user.model_dump()
        async with self.uow:
            user_id = await self.uow.users.add_one(user_dict)
            await self.uow.commit()
            return user_id

    async def get_user(self, user_id: int) -> UserSchema:
        async with self.uow:
            user = await self.uow.users.find_one(id=user_id)
            return user

    async def delete_user(self, user_id: int) -> int:
        async with self.uow:
            returned_user_id = await self.uow.users.delete_one(user_id=user_id)
            await self.uow.commit()
            return returned_user_id
