import asyncio


async def show(smp):
    await smp.acquire()
    print('Show semaphore')
    await asyncio.sleep(3)
    smp.release()


async def show_bounded(smp):
    await smp.acquire()
    print('Show semaphore')
    await asyncio.sleep(3)
    smp.release()


async def show_with(smp):
    async with smp:
        print('Show semaphore')
        await asyncio.sleep(3)


async def main():
    smp = asyncio.Semaphore(2)
    await asyncio.gather(*[show(smp) for _ in range(10)])


async def main_bounded():
    smp = asyncio.BoundedSemaphore(2)
    await asyncio.gather(*[show_bounded(smp) for _ in range(10)])


async def main_with():
    smp = asyncio.Semaphore(2)
    await asyncio.gather(*[show(smp) for _ in range(10)])

asyncio.run(main())
asyncio.run(main_with())
asyncio.run(main_bounded())
