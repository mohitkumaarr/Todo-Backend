from pydantic import BaseModel

class TodoCreate(BaseModel):
    title:str
    description:str | None = None


class TodoUpdate(BaseModel):
    title:str
    description:str | None = None
    completed: bool