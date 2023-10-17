from aiogram.filters import Filter
from aiogram.types import Message


class TextFilter(Filter):
    def __init__(self, text: str) -> None:
        self.message_text = text

    async def __call__(self, message: Message) -> bool:
        if message.text is None:
            return False
        return self.message_text.lower() == message.text.lower()
