import asyncio


async def coroutine(name):
    await asyncio.sleep(2)
    print(f'Start {name}')


async def main():
    one = asyncio.create_task(coroutine("task-1"))
    two = asyncio.create_task(coroutine("task-2"))

    await one
    await two


loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
