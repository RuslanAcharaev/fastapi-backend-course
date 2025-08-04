from typing import Optional

from pydantic import BaseModel


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None


class TaskOut(TaskIn):
    id: int
    status: bool = False
