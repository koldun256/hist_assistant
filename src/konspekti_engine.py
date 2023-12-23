import asyncio
from topic_classifier import Topic, TopicClassifier


class KonspektiEngine():
    def __init__(self, gpt):
        self.gpt = gpt
        self.topic_classifier = TopicClassifier(gpt)


    async def gen_konspekt(self, topic):
        match await self.topic_classifier.eval(topic):
            case Topic.EVENT:
                return await self.gen_event_konspekt(topic)
            case Topic.STYLE:
                return await self.gen_style_konspekt(topic)
            case Topic.PERSON:
                return await self.gen_person_konspekt(topic)
            case Topic.GENERAL:
                return await self.gen_general_konspekt(topic)
        raise Exception("Unknown topic type")


    async def gen_general_konspekt(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f"Сгенерируй конспект по истории по теме {prompt}."
            }
        ])

        return answer


    async def gen_style_konspekt(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f'Сгенерируй конспект по теме "История исскуств. {prompt}". Назови основные даты, черты. Напиши 5 самых значимых произведений этого направления.'
            }
        ])

        return answer


    async def gen_person_konspekt(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f'Сгенерируй конспект про {prompt}. Назови даты жизни, вид деятельности, основные даты биографии, вклад в историю.'
            }
        ])

        return answer


    async def gen_event_konspekt(self, prompt):
        answer = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": f"Ты хорошо знаешь историю, говоришь только про историю."
            },
            {
                "role": "user",
                "text": f'Сгенерируй конспект по по теме "Исторические события. {prompt}". Назови дату события, содержание события, причины события, следствия события, деятелей события.'
            }
        ])

        return answer
