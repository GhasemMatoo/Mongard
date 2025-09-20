from fastapi import FastAPI, Path, Query, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional, Union
from pydantic import BaseModel

import models
from schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from database import engine, SessionDatabase
from models import User

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory='templates')


def get_db():
    db = SessionDatabase()
    try:
        yield db
    finally:
        db.close()


class Person(BaseModel):
    name: str
    age: int | None = 0  # optional by python 3.10
    height: Optional[int] = 0  # optional by python 3.6
    weight: Union[int, float] = None


class Car(BaseModel):
    name: str
    model: str
    year_manufacture: int = Path(ge=2000, lt=2026)


@app.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserCreate:
    db_user = db.query(User).filter_by(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email cant be use")
    user = User(email=user.email, username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(id=user_id).first()
    if db_user:
        return db_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="use not found")


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
