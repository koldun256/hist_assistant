from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from konspekti_engine import KonspektiEngine
from enum import Enum
from quiz import Quiz


class BotState(Enum):
    KONSPEKTI = 1
    QUIZ = 2


start_msg = """Это бот, который генерирует конспекты по истории
Просто введите тему билета"""


class TelegramBot:
    state = BotState.KONSPEKTI
    quiz = None

    def __init__(self, token, gpt):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("quiz", self.quiz))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_msg))
        self.gpt = gpt
        self.konspekti_engine = KonspektiEngine(gpt)
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


    async def handle_msg(self, update, context):
        msg = update.message.text
        if self.state == BotState.KONSPEKTI:
            answer = await self.konspekti_engine.gen_konspekt(msg)
            await update.message.reply_text(answer.replace("**", "*"), parse_mode="markdown")
        elif self.state == BotState.QUIZ:
            is_correct, next_question = self.quiz.answer(msg)

            if is_correct:
                await update.message.reply_text(f"Правильно")
            else:
                await update.message.reply_text(f"Неправильно")

            await update.message.reply_text(f"Ваши баллы: {self.quiz.points}")

            if next_question is None:
                await update.message.reply_text("Конец")
                self.state = BotState.KONSPEKTI
            else:
                await update.message.reply_text(next_question.text)


    async def start(self, update, context):
        await update.message.reply_text(start_msg, parse_mode="markdown")


    async def quiz(self, update, context):
        await update.message.reply_text("Начало квиза")
        self.state = BotState.QUIZ
        self.quiz = Quiz(self.gpt, "Тест егэ по дота 2")
        first_question = self.quiz.begin()
        await update.message.reply_text(first_question)
