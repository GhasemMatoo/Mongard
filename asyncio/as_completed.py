import asyncio
import aiohttp


async def show_status(session, url, delay):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        print(f'status for {url} is {result.status}')


async def main():
    async with aiohttp.ClientSession() as session:
        requests = [show_status(session, 'https://docs.python.org/3/library/asyncio-task.html', 3),
                    show_status(session, 'https://en.wikipedia.org/wiki/Persian_language', 9),
                    show_status(session, 'https://en.wikipedia.org/wiki/Persian_Gulf', 1),
                    show_status(session, 'https://en.wikipedia.org/wiki/ljjllj', 5)
                    ]
        for rqs in asyncio.as_completed(requests):
           await rqs


asyncio.run(main())
