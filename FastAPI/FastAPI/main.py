from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def read_hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/async/")
async def root():
    return {"message": "Hello World"}


@app.get("/async/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
