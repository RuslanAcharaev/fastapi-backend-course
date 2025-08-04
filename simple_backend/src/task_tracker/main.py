from typing import Annotated

from fastapi import FastAPI, Body, HTTPException
from starlette.responses import Response, JSONResponse

from models.tasks import TaskIn, TaskDB
from external_api.api import Mockapi, Cloudflare

app = FastAPI()


@app.get("/tasks")
def get_tasks() -> list[TaskDB]:
    return Mockapi.get()


@app.post("/tasks")
def create_task(task: TaskIn) -> Response:
    description = Cloudflare.post(task.title)
    data = {'title': task.title, 'description': description}
    response = Mockapi.post(data)
    if response:
        return JSONResponse(
            status_code=201,
            content={"message": f"Задача с ID#{response['id']} успешно создана"}
        )


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_in: Annotated[TaskIn, Body()]) -> Response:
    response = Mockapi.update(task_id, task_in.model_dump_json())
    if response != 'Not found':
        return JSONResponse(
            status_code=201,
            content={"message": f"Задача c ID#{response["id"]} успешно обновлена!"}
        )
    else:
        raise HTTPException(status_code=404)


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int):
    response = Mockapi.delete(task_id)
    if response != 'Not found':
        return JSONResponse(
            status_code=200,
            content={"message": f"Задача '{response["title"]}' успешно удалена!"}
        )
    else:
        raise HTTPException(status_code=404)
