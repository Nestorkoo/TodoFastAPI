from pydantic import BaseModel

class TaskAddSchema(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskSchema(TaskAddSchema):
    id: int
        