from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

start_msg = """Это бот, который генерирует конспекты по истории
Просто введите тему билета"""

class TelegramBot:
    def __init__(self, token, gpt):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.gen_answer))
        self.gpt = gpt
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    async def gen_answer(self, update, context):
        print(update.message.text)
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f"Сгенерируй краткий конспект по истории по теме {update.message.text}. Назови основные даты, деятелей и черты."
            }
        ])

        await update.message.reply_text(answer.replace("**", "*"), parse_mode="markdown")

    def is_style(self, text):
        answer = self.gpt.sync_prompt([
            {
                "role": "system",
                "text": 'Ты разбираешься в истории искусств. Ты отвечаешь на вопрос только "да" или "нет".'
            },
            {
                "role": "user",
                "text": f'Существует ли направление в живописи "{text}"? Ответь да или нет.'
            }
        ], max_tokens = 10)

        return 'да' in answer or 'Да' in answer

    async def start(self, update, context):
        await update.message.reply_text(start_msg, parse_mode="markdown")
