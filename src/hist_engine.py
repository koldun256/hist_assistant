from enum import Enum
import asyncio

class Theme(Enum):
    EVENT=1
    STYLE=2
    GENERAL=3

class HistEngine():
    def __init__(self, gpt):
        self.gpt = gpt


    async def classify_theme(self, theme):
        is_event, is_style = await asyncio.gather(
            self._is_event(theme),
            self._is_style(theme),
        ) 
        if is_event:
            return Theme.EVENT
        if is_style:
            return Theme.STYLE
        return Theme.GENERAL

    
    async def gen_konspekti(self, theme):
        match await self.classify_theme(theme):
            case Theme.EVENT:
                return await self.gen_event_konspekti(theme)
            case Theme.STYLE:
                return await self.gen_style_konspekti(theme)
            case Theme.GENERAL:
                return await self.gen_general_konspekti(theme)
        raise Exception("Unkonwn theme type")


    async def _is_style(self, text):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": 'Ты разбираешься в истории искусств. Ты отвечаешь на вопрос только "да" или "нет".'
            },
            {
                "role": "user",
                "text": f'Существует ли направление в живописи "{text}"? Ответь да или нет.'
            }
        ], max_tokens = 10, model="yandexgpt-lite", timeout=2)

        return 'да' in answer or 'Да' in answer
    

    async def _is_event(self, text):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": 'Ты разбираешься в истории. Ты отвечаешь на вопрос только "да" или "нет".'
            },
            {
                "role": "user",
                "text": f'"{text}" - это историческое событие? Ответь да или нет.'
            }
        ], max_tokens=10, model="yandexgpt-lite", timeout=2)

        return 'да' in answer or 'Да' in answer


    async def gen_general_konspekti(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f"Сгенерируй краткий конспект по истории по теме {prompt}. Назови основные даты, деятелей и черты."
            }
        ])

        return answer


    async def gen_style_konspekti(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f'Сгенерируй краткий конспект по по теме "История исскуств. {prompt}". Назови основные даты, черты. Напиши 5 самых значимых произведений этого направления.'
            }
        ])

        return answer


    async def gen_event_konspekti(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f'Сгенерируй краткий конспект по по теме "Исторические события. {prompt}". Назови дату события, содержание события, причины события, следствия события, деятелей события.'
            }
        ])

        return answer
