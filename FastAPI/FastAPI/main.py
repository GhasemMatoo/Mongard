from fastapi import FastAPI, Path, Query, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional, Union
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class Person(BaseModel):
    name: str
    age: int | None = 0  # optional by python 3.10
    height: Optional[int] = 0  # optional by python 3.6
    weight: Union[int, float] = None


class Car(BaseModel):
    name: str
    model: str
    year_manufacture: int = Path(ge=2000, lt=2026)


class User(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str


@app.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User) -> User:
    if user.username == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username cant be admin")
    return user


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


@app.get("/home/{username}", response_class=HTMLResponse)
async def index(request: Request, username: str) -> HTMLResponse:
    return templates.TemplateResponse('home.html', context={"request": request, "username": username})
