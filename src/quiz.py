class Question():
    def __init__(self, topic, text):
        self.topic = topic
        self.text = text

    
    def test_answer(self, answer):
        return answer != "Нет"


class Quiz():
    current_question = None
    points = 0


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
                "text": f'Сгенерируй три вопроса по теме {topic}.'
            }
        ], timeout=4)
        print(questions)
        return [Question(self.topic, question) for question in questions.split('\n')]


    def answer(self, answer_text):
        correct = self.current_question.test_answer(answer_text)
        if correct:
            self.points += 1

        if len(self.questions) == 0:
            return correct, None

        self.current_question = self.questions.pop(0)
        return correct, self.current_question
