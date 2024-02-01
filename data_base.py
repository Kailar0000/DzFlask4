from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    text: str
    complit: bool

