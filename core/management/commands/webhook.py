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
from aiohttp import web 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import logging
from core.tasks import send_file

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    level=logging.INFO
)


# Webserver settings
# bind localhost only to prevent any external access
WEB_SERVER_HOST = "127.0.0.1"
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = 8081
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "my-secret"
BASE_WEBHOOK_URL = "https://bot.thevirgoent.com"
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
                message.answer('Visit the channel @udpcustom')



        async def on_startup(bot: Bot) -> None:
            await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

        def main(): 
            dp = Dispatcher()
            dp.include_router(router)
            dp.startup.register(on_startup)
            # Create aiohttp.web.Application instance
            app = web.Application()
            webhook_requests_handler = SimpleRequestHandler(
                dispatcher=dp,
                bot=bot,
                secret_token=WEBHOOK_SECRET,
            )
            # Register webhook handler on application
            webhook_requests_handler.register(app, path=WEBHOOK_PATH)

            # Mount dispatcher startup and shutdown hooks to aiohttp application
            setup_application(app, dp, bot=bot)

            # And finally start webserver
            web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
