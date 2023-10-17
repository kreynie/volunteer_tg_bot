import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import settings
from routers import all_routers


async def main():
    bot: Bot = Bot(settings.token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp: Dispatcher = Dispatcher()
    dp.include_routers(*all_routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
