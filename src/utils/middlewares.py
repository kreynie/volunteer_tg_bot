from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.services.users import UsersService
from src.utils.dependencies import UOWDep


class AuthorizedCommandsMiddleware(BaseMiddleware):
    def __init__(self, uow: UOWDep, authority_level: int) -> None:
        self.uow = uow
        self.authority_level = authority_level

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        is_authorized = await (UsersService(self.uow)
                               .check_rights(user_tg_id=user_id,
                                             required_rights=self.authority_level))
        if is_authorized:
            return await handler(event, data)
