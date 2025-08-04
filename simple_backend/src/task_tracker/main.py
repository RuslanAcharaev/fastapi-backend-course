from itertools import count
from typing import Annotated

from fastapi import FastAPI, Body
from starlette.responses import Response, JSONResponse

from models.tasks import TaskIn, TaskDB

app = FastAPI()

id_generator = count()

tasks = []


@app.get("/tasks")
def get_tasks() -> list[TaskDB]:
    return tasks


@app.post("/tasks")
def create_task(task: TaskIn) -> Response:
    id = next(id_generator)
    new_task = TaskDB(
        id=id, title=task.title, description=task.description, status=task.status,
    )
    tasks.append(new_task)
    return JSONResponse(status_code=201, content={"message": f"Задача '{task.title}' c ID#{id} успешно создана!"})


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_in: Annotated[TaskIn, Body()]) -> Response:
    for task in tasks:
        if task.id == task_id:
            task.title = task_in.title
            task.description = task_in.description
            task.status = task_in.status
            return JSONResponse(status_code=201, content={"message": f"Задача '{task.title}' c ID#{task_id} успешно обновлена!"})


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Задача успешно удалена"}
