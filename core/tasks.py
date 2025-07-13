from celery import shared_task  
from django.conf import settings
from django.shortcuts import get_object_or_404   
from .models import *   
import logging   
from core.models import File
from telepot import Bot, glance
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
TOKEN = settings.BOT_TOKEN
bot = Bot(TOKEN)#this is telepot
channel_id=settings.CHANNEL_ID

logger = logging.getLogger(__name__)

@shared_task
def send_to_channel(file_id):

    try:
        file=get_object_or_404(File, pk=file_id)
    except:
        file=None

    if file:
        inline_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📥Get Config", url=f"http://t.me/{settings.BOT_NAME}?start={file_id}"),
                InlineKeyboardButton(text="Get Premium⭐️", url=f"http://t.me/teslassh")
            ]
        ])

        with open("static/ad.jpg", "rb") as photo:
    
            send_it = bot.sendPhoto(
                chat_id=channel_id,
                photo=photo,
                caption=(
                    f"🔗File: {file.name}\n\n"
                    f"✍️ {file.description}\n\n"
                    f"#UDPCUSTOM #EthicalNetworking\n\n"
                    f"╰┈➤ ᴅᴏɴᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ʀᴇᴀᴄᴛ 👍💖"
                ),
                parse_mode='HTML',
                reply_markup=inline_keyboard2
            )
    else:
        return

@shared_task
def send_file(user_id, file_id):
    file=File.objects.get(pk=file_id)
    file_path = file.path.path

    with open(file_path, "rb") as fi:
 
        send_it = bot.sendDocument(
            chat_id=user_id,
            document=fi,
            caption=(
                f"🔗File Name: {file.name}\n\n"
                
            ),
            parse_mode='HTML'
        )