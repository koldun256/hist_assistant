from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class TelegramBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(MessageHandler(filters.TEXT, self.echo))
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    async def echo(self, update, context):
        await update.message.reply_text(update.message.text)

