from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from konspekti_engine import KonspektiEngine


start_msg = """Это бот, который генерирует конспекты по истории
Просто введите тему билета"""


class TelegramBot:
    def __init__(self, token, gpt):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_msg))
        self.konspekti_engine = KonspektiEngine(gpt)
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


    async def handle_msg(self, update, context):
        msg = update.message.text
        answer = await self.konspekti_engine.gen_konspekt(msg)

        await update.message.reply_text(answer.replace("**", "*"), parse_mode="markdown")


    async def start(self, update, context):
        await update.message.reply_text(start_msg, parse_mode="markdown")
