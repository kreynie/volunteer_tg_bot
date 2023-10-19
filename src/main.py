import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import project_path, settings
from routers import all_routers
from src.utils.middlewares import AuthorizedCommandsMiddleware
from src.utils.unitofwork import UnitOfWork


async def main():
    bot: Bot = Bot(settings.token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp: Dispatcher = Dispatcher()
    dp.include_routers(*all_routers)
    dp.message.middleware(AuthorizedCommandsMiddleware(
        uow=UnitOfWork(),
        authority_level=0,
    ))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log_handler = logging.FileHandler(project_path.parent / "debug.log")
    log_handler.setFormatter(logging.Formatter("{asctime} {levelname} {message}", style="{"))
    logging.getLogger().addHandler(log_handler)
    asyncio.run(main())
