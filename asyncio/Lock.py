import asyncio

counter = 0
counter_by_with = 0


async def increment(lock):
    global counter
    await lock.acquire()
    temp_counter = counter
    temp_counter += 1
    await asyncio.sleep(0.01)
    counter = temp_counter
    lock.release()


async def increment_by_with(lock):
    global counter_by_with
    async with lock:
        temp_counter = counter_by_with
        temp_counter += 1
        await asyncio.sleep(0.01)
        counter_by_with = temp_counter


async def main():
    lock = asyncio.Lock()
    global counter
    tasks = [asyncio.create_task(increment(lock)) for _ in range(100)]
    await asyncio.gather(*tasks)
    print(f'Counter is {counter}')


async def main_by_with():
    lock = asyncio.Lock()
    global counter
    tasks = [asyncio.create_task(increment_by_with(lock)) for _ in range(100)]
    await asyncio.gather(*tasks)
    print(f'Counter is {counter}')


asyncio.run(main())

asyncio.run(main_by_with())
