class HistEngine():
    def __init__(self, gpt):
        self.gpt = gpt

    async def gen_konspekti(self, prompt):
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
