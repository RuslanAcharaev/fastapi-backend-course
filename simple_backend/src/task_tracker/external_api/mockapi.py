import requests
from environs import Env

env = Env()
env.read_env()
url=env("MOCKAPI_URL")
headers = {"Content-Type": "application/json"}


class Tasks:
    @staticmethod
    def get_tasks():
        response = requests.get(f'{url}/tasks')
        return response.json()

    @staticmethod
    def add_task(task):
        response = requests.post(f'{url}/tasks', headers=headers, data=task)
        return response.json()

    @staticmethod
    def update_task(task_id, task):
        response = requests.put(f'{url}/tasks/{task_id}', headers=headers, data=task)
        return response.json()

    @staticmethod
    def delete_task(task_id):
        response = requests.delete(f'{url}/tasks/{task_id}', headers=headers)
        return response.json()
