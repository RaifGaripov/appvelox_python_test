from datetime import date

from pydantic import BaseModel


class TaskBase(BaseModel):
    header: str
    text: str
    completion_date: date


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    is_completed: bool

    class Config:
        orm_mode = True
