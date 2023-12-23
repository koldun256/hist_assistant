from enum import Enum
import asyncio

class Topic(Enum):
    EVENT=1
    STYLE=2
    PERSON=3
    GENERAL=4

class TopicClassifier():
    def __init__(self, gpt):
        self.gpt = gpt


    async def eval(self, topic):
        is_person, is_event, is_style = await asyncio.gather(
            self.is_person(topic),
            self.is_event(topic),
            self.is_style(topic),
        ) 
        if is_person:
            return Topic.PERSON
        if is_event:
            return Topic.EVENT
        if is_style:
            return Topic.STYLE
        return Topic.GENERAL


    async def is_style(self, text):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": 'Ты разбираешься в истории искусств. Ты отвечаешь на вопрос только "да" или "нет".'
            },
            {
                "role": "user",
                "text": f'"{text}" - это культурное течение? Ответь да или нет.'
            }
        ], max_tokens = 10, model="yandexgpt-lite")

        print("Is Style: ", answer)

        return 'да' in answer or 'Да' in answer
    

    async def is_event(self, text):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": 'Ты разбираешься в истории. Ты отвечаешь на вопрос только "да" или "нет".'
            },
            {
                "role": "user",
                "text": f'"{text}" - это историческое событие? Ответь да или нет.'
            }
        ], max_tokens=10, model="yandexgpt-lite")

        print("Is Event: ", answer)

        return 'да' in answer or 'Да' in answer


    async def is_person(self, text):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": 'Ты разбираешься в истории. Ты отвечаешь на вопрос только "да" или "нет".'
            },
            {
                "role": "user",
                "text": f'"{text}" - это исторический деятель? Ответь да или нет.'
            }
        ], max_tokens=10, model="yandexgpt-lite")

        print("Is Person: ", answer)

        return 'да' in answer or 'Да' in answer
