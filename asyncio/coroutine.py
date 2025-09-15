import asyncio
import datetime


async def coroutine(name):
    await asyncio.sleep(2)
    print(f'Hello {name}')


async def main():
    a = asyncio.create_task(coroutine("one"))
    b = asyncio.create_task(coroutine("two"))

    await a
    await b


print(f"Start ===> {datetime.datetime.now()}")
asyncio.run(main())
print(f"End ===> {datetime.datetime.now()}")
