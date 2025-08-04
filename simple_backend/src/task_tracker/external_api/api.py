import json
import requests
from environs import Env

env = Env()
env.read_env()
url = env("MOCKAPI_URL")
api_key = env("CF_API_TOKEN")
account_id = env("CF_ACCOUNT_ID")
headers = {"Content-Type": "application/json"}


class Mockapi:
    @staticmethod
    def get():
        response = requests.get(f'{url}/tasks')
        return response.json()

    @staticmethod
    def post(task):
        data = json.dumps(task)
        response = requests.post(f'{url}/tasks', headers=headers, data=data)
        return response.json()

    @staticmethod
    def update(task_id, task):
        response = requests.put(f'{url}/tasks/{task_id}', headers=headers, data=task)
        return response.json()

    @staticmethod
    def delete(task_id):
        response = requests.delete(f'{url}/tasks/{task_id}', headers=headers)
        return response.json()


class Cloudflare:
    @staticmethod
    def post(title):
        inputs = [
            {"role": "system", "content": "Ты дружелюбный ассистент, который помогает решать различного рода задачи"},
            {"role": "user",
             "content": f"Передо мной поставлена задача: '{title}'. Расскажи кратко, как мне её решить."},
        ]
        input = {"messages": inputs}
        header = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        cf_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/qwen/qwen1.5-0.5b-chat"
        response = requests.post(cf_url, headers=header, json=input)
        data = response.json()
        return data['result']['response']
