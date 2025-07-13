from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime as dtm, timezone as tzn 
from django.shortcuts import get_object_or_404 
from django.utils import timezone 
import datetime 
from asgiref.sync import sync_to_async   
import sys   
from aiogram import Dispatcher, Bot, F, Router
import asyncio
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton 
from aiogram.types.input_file import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
) 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 
import logging
from core.tasks import send_file

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    level=logging.INFO
)

router = Router()
ADMINS = [6921553302] 
TOKEN = settings.BOT_TOKEN
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

pm = ParseMode.MARKDOWN_V2

class Command(BaseCommand):
    help = 'Channel Manager Bot'

    def handle(self, *_, **__):
        @router.message(F.text.lower().startswith('/start'))
        async def other_responses(message: Message):
            """
            Handles other messages in the system bot. things like the start command and all its args
            """
            msg = message.text
            user = message.from_user
            chat_id = user.id 
 
            if len(msg.split()) == 2:
                file_id = msg.split()[1]
                await sync_to_async(send_file.delay)(chat_id, file_id)
            else:
                await message.answer('Visit the channel @udpcustom')

        async def main():
            dp = Dispatcher()
            dp.include_router(router)
            
            # Start polling instead of webhook
            await bot.delete_webhook()  # Ensure webhook is removed
            await dp.start_polling(bot)

        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())