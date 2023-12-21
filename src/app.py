from dotenv import load_dotenv
import os
from gpt_wrapper import GPTWrapper

load_dotenv()

yc_folder_id = os.getenv("YC_FOLDER_ID")
yc_iam_token = os.getenv("YC_IAM_TOKEN")



gpt = GPTWrapper(yc_folder_id, yc_iam_token)
print(gpt.prompt([
    {
        "role": "system",
        "text": "Напиши краткий конспект по истории"
    },
    {
        "role": "user",
        "text": "Барокко"
    }
]))
