from typing import Optional

from pydantic import BaseModel


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None


class TaskDB(TaskIn):
    id: int
    status: bool = False
