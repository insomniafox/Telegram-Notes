from aiogram.types import Message
from api_client.client import NotesAPIClient
import structlog

logger = structlog.get_logger(__name__)


async def get_notes_handler(message: Message):
    user_id = message.from_user.id
    notes = await NotesAPIClient.get_notes(user_id)
    await message.reply(str(notes))
