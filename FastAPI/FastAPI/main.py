from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, Union, Tuple
from pydantic import BaseModel

app = FastAPI()


class Person(BaseModel):
    name: str
    age: int | None = 0  # optional by python 3.10
    height: Optional[int] = 0  # optional by python 3.6
    weight: Union[int, float] = None


class Car(BaseModel):
    name: str
    model: str
    year_manufacture: int = Path(ge=2000, lt=2026)


@app.post("/car/")
async def read_car(
        car: Car, alias_name: str = Query(default="nothing", max_length=20, min_length=7)) -> tuple[Car, str]:
    return car, alias_name


@app.post("/person/")
async def reade_person(person: Person) -> Person:
    return person


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def read_hello(name: str, age: int = 0) -> dict:
    # name == Path Parameter
    # age == Query Parameter
    return {"message": f"Hi {name}, you are {age} years"}


@app.get("/async/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/async/hello/{name}")
async def say_hello(name: str, age: int = 0) -> dict:
    # name == Path Parameter
    # age == Query Parameter
    return {"message": f"Hi {name}, you are {age} years"}
