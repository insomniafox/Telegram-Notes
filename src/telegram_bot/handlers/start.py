from aiogram.filters import CommandObject
from aiogram.types import Message
from api_client.client import NotesAPIClient
from api_client.exceptions import NotesAPIException
import structlog

logger = structlog.get_logger(__name__)


async def start_handler(message: Message, command: CommandObject):
    token = command.args
    if not token:
        await message.reply("Вы не предоставили токен.")
        return
    user_id = message.from_user.id
    try:
        await NotesAPIClient.link_telegram_id(token, user_id)
    except NotesAPIException as e:
        logger.error('Error occurred!', error=str(e))
        await message.reply("Что-то пошло не так. Попробуйте снова позже.")
