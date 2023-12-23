from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from konspekti_engine import KonspektiEngine
from chats import ChatDB, ChatState
from enum import Enum
from quiz import Quiz

start_msg = """Это бот, который генерирует конспекты по истории
Просто введите тему билета"""


class TelegramBot:
    def __init__(self, token, gpt):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("quiz", self.quiz))
        self.app.add_handler(CommandHandler("konspekti", self.konspekti))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_msg))
        self.gpt = gpt
        self.chat_db = ChatDB()
        self.konspekti_engine = KonspektiEngine(gpt)
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


    async def konspekti(self, update, context):
        if len(context.args) == 0:
            await update.message.reply_text("Использование: /konspekti <тема_конспекта>")
            return
        chat = self.chat_db.get(update.message.chat_id)
        if chat.state == ChatState.MENU:
            answer = await self.konspekti_engine.gen_konspekt(" ".join(context.args))
            await update.message.reply_text(answer.replace("**", "*"), parse_mode="markdown")
        else:
            await update.message.reply_text("Сначала закончите квиз")


    async def handle_msg(self, update, context):
        msg = update.message.text
        chat = self.chat_db.get(update.message.chat_id)
        if chat.state == ChatState.MENU:
            await update.message.reply_text("Введи команду")
        elif chat.state == ChatState.QUIZ:
            review, next_question = await chat.quiz.answer(msg)

            await update.message.reply_text(review)

            if next_question is None:
                await update.message.reply_text("Конец квиза")
                chat.state = ChatState.MENU
            else:
                await update.message.reply_text(f"Вопрос {5 - len(chat.quiz.questions)}. {next_question.text}")


    async def start(self, update, context):
        await update.message.reply_text(start_msg, parse_mode="markdown")


    async def quiz(self, update, context):
        if len(context.args) == 0:
            await update.message.reply_text("Использование: /quiz <тема_квиза>")
            return
        chat = self.chat_db.get(update.message.chat_id)
        await update.message.reply_text("Начало квиза")
        chat.state = ChatState.QUIZ
        chat.quiz = Quiz(self.gpt, " ".join(context.args))
        first_question = await chat.quiz.begin()
        await update.message.reply_text(f"Вопрос {5 - len(chat.quiz.questions)}. {first_question}")
