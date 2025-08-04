import json
from ..models.tasks import TaskDB

class Tasks:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                return [TaskDB(**task) for task in tasks_data]
        except FileNotFoundError:
            return []

    def _save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.model_dump() for task in self.tasks], file, ensure_ascii=False)

    def add_task(self, task):
        self.tasks.append(task)
        self._save_tasks()

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self._save_tasks()
                return True
        return False

    def get_id(self):
        if not self.tasks:
            return 0
        next_id = self.tasks[-1].id + 1
        return next_id