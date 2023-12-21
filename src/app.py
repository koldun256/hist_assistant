from dotenv import load_dotenv
import os
import requests

load_dotenv()

yc_folder_id = os.getenv("YC_FOLDER_ID")
yc_iam_token = os.getenv("YC_IAM_TOKEN")

print("folder_id: ", yc_folder_id)
print("IAM Token: ", yc_iam_token)

req_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

req_payload = {
    "modelUri": f"gpt://{yc_folder_id}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [{
        "role": "system",
        "text": "Напиши конспект по истории"
    }, {
        "role": "user",
        "text": "Барокко"
    }]
}

req_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {yc_iam_token}",
    "x-folder-id": yc_folder_id
}

res = requests.post(req_url, json=req_payload, headers=req_headers)
print(res.text)
