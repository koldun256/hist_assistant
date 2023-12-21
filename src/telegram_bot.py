from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

start_msg = """Это бот который генерирует конспекты по истории
Просто введите тему билета"""

class TelegramBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    async def echo(self, update, context):
        await update.message.reply_text(update.message.text)

    async def start(self, update, context):
        await update.message.reply_text(start_msg)
