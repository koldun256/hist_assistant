from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from konspekti_engine import KonspektiEngine
from chats import ChatDB, ChatState
from enum import Enum
from quiz import Quiz

help_msg = """Савелий -- бот, который поможет тебе подготовится к экзамену по истории.
Он умеет генерировать конспекты и тестировать твои знания.
Список доступных команд:
/help -- вывести это сообщение
/konspekti <тема конспекта> -- сгенерировать конспект на заданную тему
/quiz <тема квиза> -- проверить свои знания по заданной теме
/exit_quiz -- прервать квиз"""


class TelegramBot:
    def __init__(self, token, gpt):
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.help))
        self.app.add_handler(CommandHandler("quiz", self.quiz))
        self.app.add_handler(CommandHandler("exit_quiz", self.exit_quiz))
        self.app.add_handler(CommandHandler("konspekti", self.konspekti))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_msg))
        self.gpt = gpt
        self.chat_db = ChatDB()
        self.konspekti_engine = KonspektiEngine(gpt)
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


    async def help(self, update, context):
        await update.message.reply_text(help_msg)


    async def konspekti(self, update, context):
        if len(context.args) == 0:
            await update.message.reply_text("Использование: /konspekti <тема_конспекта>")
            return
        chat = self.chat_db.get(update.message.chat_id)
        if chat.state == ChatState.MENU:
            zadumalsya = await update.message.reply_text("Савелий задумался...")
            answer = await self.konspekti_engine.gen_konspekt(" ".join(context.args))
            await zadumalsya.delete()
            await update.message.reply_text(answer.replace("**", "*"), parse_mode="markdown")
        else:
            await update.message.reply_text("Сначала закончите квиз")


    async def handle_msg(self, update, context):
        msg = update.message.text
        chat = self.chat_db.get(update.message.chat_id)
        if chat.state == ChatState.MENU:
            await update.message.reply_text("/help -- вывод справки")
        elif chat.state == ChatState.QUIZ:
            zadumalsya = await update.message.reply_text("Савелий задумался...")
            review, next_question = await chat.quiz.answer(msg)

            await update.message.reply_text(review)

            if next_question is None:
                await update.message.reply_text("Конец квиза")
                chat.state = ChatState.MENU
                chat.quiz = None
            else:
                await update.message.reply_text(f"Вопрос {5 - len(chat.quiz.questions)}. {next_question.text}")
            await zadumalsya.delete()

    
    async def exit_quiz(self, update, context):
        chat = self.chat_db.get(update.message.chat_id)
        chat.quiz = None
        chat.state = ChatState.MENU
        await update.message.reply_text("Конец квиза")


    async def quiz(self, update, context):
        if len(context.args) == 0:
            await update.message.reply_text("Использование: /quiz <тема_квиза>")
            return
        zadumalsya = await update.message.reply_text("Савелий задумался...")
        chat = self.chat_db.get(update.message.chat_id)
        await update.message.reply_text("Начало квиза")
        chat.state = ChatState.QUIZ
        chat.quiz = Quiz(self.gpt, " ".join(context.args))
        first_question = await chat.quiz.begin()
        await update.message.reply_text(f"Вопрос {5 - len(chat.quiz.questions)}. {first_question}")
        await zadumalsya.delete()
