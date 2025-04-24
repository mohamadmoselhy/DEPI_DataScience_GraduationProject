# Example Pydantic or ORM model

from pydantic import BaseModel

class InputModel(BaseModel):
    name: str
    age: int
