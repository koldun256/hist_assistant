from enum import Enum


class ChatState(Enum):
    MENU = 1
    QUIZ = 2


class Chat():
    state = ChatState.MENU
    quiz = None

    def __init__(self, chat_id):
        self.chat_id = chat_id


class ChatDB():
    def __init__(self):
        self.chats = []
        

    def get(self, chat_id):
        try:
            return next(chat for chat in self.chats if chat.chat_id == chat_id)
        except StopIteration:
            print("creating new chat!! yay")
            new_chat = Chat(chat_id)
            self.chats.append(new_chat)
            return new_chat
