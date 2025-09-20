from pydantic import BaseModel
from typing import Optional, Union


class Person(BaseModel):
    name: str
    age: int | None = 0  # optional by python 3.10
    height: Optional[int] = 0  # optional by python 3.6
    weight: Union[int, float] = None
