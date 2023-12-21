import requests
import json

class GPTWrapper():
    def __init__(self, folder_id, iam_token):
        self.folder_id = folder_id
        self.iam_token = iam_token
    
    def prompt(self, messages, temperature=0.6, max_tokens=2000):
        req_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

        req_payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": max_tokens
            },
            "messages": messages
        }

        req_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.iam_token}",
            "x-folder-id": self.folder_id
        }

        res = requests.post(req_url, json=req_payload, headers=req_headers)

        return json.loads(res.text)["result"]["alternatives"][0]["message"]["text"]

