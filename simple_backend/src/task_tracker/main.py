import json
from typing import Annotated

from fastapi import FastAPI, Body
from starlette.responses import Response, JSONResponse

from models.tasks import TaskIn, TaskDB

app = FastAPI()


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


tasks = Tasks()


@app.get("/tasks")
def get_tasks() -> list[TaskDB]:
    return tasks.tasks


@app.post("/tasks")
def create_task(task: TaskIn) -> Response:
    next_id = tasks.get_id()
    new_task = TaskDB(
        id=next_id, title=task.title, description=task.description, status=task.status,
    )
    tasks.add_task(new_task)
    return JSONResponse(status_code=201, content={"message": f"Задача '{task.title}' c ID#{id} успешно создана!"})


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_in: Annotated[TaskIn, Body()]) -> Response:
    for task in tasks.tasks:
        if task.id == task_id:
            task.title = task_in.title
            task.description = task_in.description
            task.status = task_in.status
            return JSONResponse(status_code=201,
                                content={"message": f"Задача '{task.title}' c ID#{task_id} успешно обновлена!"})


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int):
    if tasks.delete_task(task_id):
        return {"message": "Задача успешно удалена"}
