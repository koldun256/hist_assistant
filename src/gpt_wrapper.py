import requests
import json
import time

class GPTWrapper():
    def __init__(self, folder_id, iam_token):
        self.folder_id = folder_id
        self.iam_token = iam_token
    
    def get_async_result(self, req_id):
        req_url = f"https://llm.api.cloud.yandex.net/operations/{req_id}"

        req_headers = {
            "Authorization": f"Bearer {self.iam_token}",
        }

        res = requests.get(req_url, headers=req_headers)
        try:
            return json.loads(res.text)["response"]["alternatives"][0]["message"]["text"]
        except:
            print("not enought time!!!")
            print(res.text)
            return False

    async def async_prompt(self, messages, temperature=0.6, max_tokens=2000, model="yandexgpt"):
        req_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"

        req_payload = {
            "modelUri": f"gpt://{self.folder_id}/{model}",
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
        time.sleep(10)
        req_id = json.loads(res.text)["id"]
        return self.get_async_result(req_id)

    def sync_prompt(self, messages, temperature=0.6, max_tokens=2000, model="yandexgpt-lite"):
        req_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

        req_payload = {
            "modelUri": f"gpt://{self.folder_id}/{model}",
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
        print(res.text)
        return json.loads(res.text)["result"]["alternatives"][0]["message"]["text"]

