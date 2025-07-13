import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.conf import settings
from asgiref.sync import sync_to_async 
from django.utils import timezone 
from core.models import File
import datetime 
from datetime import timedelta  

 
TOKEN = settings.BOT_TOKEN
Channel_id_arr = settings.CHANNEL_ID
botname = settings.BOT_NAME

pm = ParseMode.MARKDOWN_V2

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    level=logging.INFO
)

class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **options): 
        #this must take effect in a direct chat(DM)
        async def poll_the_db(context: ContextTypes.DEFAULT_TYPE) -> None:
            unsent_files = await sync_to_async(lambda: list(File.objects.filter(sent=False)))()
            print(unsent_files)

            for file in unsent_files:
                for Channel_id in Channel_id_arr:
                    file_id = file.id
                    description = file.description
                    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="⏬ Download File", url=f'http://t.me/{botname}?start={file_id}'),
                             InlineKeyboardButton(text="⚡️Inquire", url="https://t.me/teslasshx")], 
                        ])
                    
                    mosaad = f"🔗File Name: {file.name}\n\n✍️ {description}\n\n#UDPCUSTOM #WIPI_BOT\n\n╰┈➤ ᴅᴏɴᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ʀᴇᴀᴄᴛ 👍💖"

                    nora = await context.bot.send_message(
                                chat_id=Channel_id,
                                text = mosaad,
                                parse_mode='HTML',
                                reply_markup=inline_keyboard
                            )
            # Mark the file as sent
                file.sent = True
                await sync_to_async(file.save)()

            #        with open(ad.photo.path, 'rb') as photo:
              #                      nora = await context.bot.send_photo(
              #                          chat_id=Channel_id,
             #                           photo=photo,
              #                          caption=description,
              #                          parse_mode='HTML',
               #                         reply_markup=inline_keyboard
               #                     )






        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            """Handle the /start command."""
            user = update.effective_user
            chat_id = update.effective_chat.id
            username = update.effective_chat.username

            if context.args:
                file_id = context.args[0]

                try:
                    file = await sync_to_async(get_object_or_404)(File, id=file_id)
                except  Exception as e:
                    file = None

                if file:
                    file_path = file.path.path

                    with open(file_path, 'rb') as f:
                            await context.bot.send_document(
                                chat_id=chat_id,
                                document=f,
                                caption= f"⭐️ʀᴇᴍᴀʀᴋꜱ: {file.name}\n\n ╰┈➤ ᴅᴏɴᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ʀᴇᴀᴄᴛ 👍💖 ᴏɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴘᴏꜱᴛꜱ\n\nBy: @teslasshx",
                            )
                else:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="❌ File Nolonger exists.",
                    )
                        
                   

                    
                

        # Start the bot with Application
        application = Application.builder().token(TOKEN).build() 

        # Schedule the job to check for expired timers every 20 seconds
        application.job_queue.run_repeating(poll_the_db, interval=5, first=4)
        application.add_handler(CommandHandler("start", start))


        application.run_polling()

if __name__ == '__main__':
    main()