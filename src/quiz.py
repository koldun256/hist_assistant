class Question():
    def __init__(self, gpt, topic, text):
        self.topic = topic
        self.text = text
        self.gpt = gpt

    
    async def test_answer(self, answer):
        review = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": "Представь что ты проверяешь тест по истории"
            },
            {
                "role": "user",
                "text": f'Является ли ответ "{answer}" на вопрос "{self.text}" правильным? Оцени ответ. В случае неправильного ответа укажи правильный.'
            }
        ])

        return review


class Quiz():
    current_question = None


    def __init__(self, gpt, topic):
        print(f"New quiz with topic {topic}!")
        self.gpt = gpt
        self.topic = topic


    async def begin(self):
        self.questions = await self.gen_questions(self.topic)
        self.current_question = self.questions.pop(0)
        return self.current_question.text


    async def gen_questions(self, topic):
        questions = await self.gpt.async_prompt([
            {
                "role": "system",
                "text": "Представь что ты автор теста по истории."
            },
            {
                "role": "user",
                "text": f'Сгенерируй пять вопросов по теме {topic}.'
            }
        ], timeout=4)

        return [Question(self.gpt, self.topic, question) \
                for question \
                in questions.split('\n') \
                if len(question) > 2]


    async def answer(self, answer_text):
        review = await self.current_question.test_answer(answer_text)

        if len(self.questions) == 0:
            return review, None

        self.current_question = self.questions.pop(0)
        return review, self.current_question
