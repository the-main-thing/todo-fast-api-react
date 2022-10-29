from pydantic import BaseModel


class Todo(BaseModel):
    key: int
    text: str
    done: bool
