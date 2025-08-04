from typing import Optional

from pydantic import BaseModel


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False


class TaskDB(TaskIn):
    id: int
