from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

start_msg = """Это бот который генерирует конспекты по истории
Просто введите тему билета"""

class TelegramBot:
    def __init__(self, token, gpt):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.gen_answer))
        self.gpt = gpt
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    async def gen_answer(self, update, context):
        answer = self.gpt.prompt([
            {
                "role": "system",
                "text": "Ты учитель истории, который даёт конспекты по заданным темам"
            },
            {
                "role": "user",
                "text": update.message.text
            }
        ])
        await update.message.reply_text(answer)

    async def start(self, update, context):
        await update.message.reply_text(start_msg)
