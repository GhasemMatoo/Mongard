from fastapi import Query, HTTPException, status, Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas.users import UserCreate, UserResponse
from schemas.person import Person
from schemas.car import Car
from sqlalchemy.orm import Session
from models.users import User
from dependencies import get_db

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserCreate:
    db_user = db.query(User).filter_by(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email cant be use")
    user = User(email=user.email, username=user.username, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(id=user_id).first()
    if db_user:
        return db_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="use not found")


@router.post("/car/")
async def read_car(
        car: Car, alias_name: str = Query(default="nothing", max_length=20, min_length=7)) -> tuple[Car, str]:
    return car, alias_name


@router.post("/person/")
async def reade_person(person: Person) -> Person:
    return person


@router.get("/")
def read_root() -> dict:
    return {"message": "Hello World"}


@router.get("/hello/{name}")
def read_hello(name: str, age: int = 0) -> dict:
    # name == Path Parameter
    # age == Query Parameter
    return {"message": f"Hi {name}, you are {age} years"}


@router.get("/async/")
async def root() -> dict:
    return {"message": "Hello World"}


@router.get("/async/hello/{name}")
async def say_hello(name: str, age: int = 0) -> dict:
    # name == Path Parameter
    # age == Query Parameter
    return {"message": f"Hi {name}, you are {age} years"}


@router.get("/home/{username}", response_class=HTMLResponse)
async def index(request: Request, username: str) -> HTMLResponse:
    return templates.TemplateResponse('home.html', context={"request": request, "username": username})
