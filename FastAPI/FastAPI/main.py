from fastapi import FastAPI
from routers import user
from datetime import datetime
import time

app = FastAPI()
app.include_router(user.router, tags=["all"])


@app.middleware('http')
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.on_event('startup')
async def startup_event():
    with open('server_time_log.log', 'a') as log:
        log.write(f'Server started at:{datetime.now()} \n')


@app.on_event('shutdown')
async def shutdown_event():
    with open('server_time_log.log', 'a') as log:
        log.write(f'Server shut down at:{datetime.now()} \n')
