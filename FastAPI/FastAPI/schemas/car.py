from fastapi import Path
from pydantic import BaseModel


class Car(BaseModel):
    name: str
    model: str
    year_manufacture: int = Path(ge=2000, lt=2026)
