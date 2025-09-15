import asyncio
import aiohttp


async def show_status(session, url):
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://docs.python.org/3/library/asyncio-task.html'
        status = await show_status(session, url)
        print(f'status is {status}')


async def main_tow():
    async with aiohttp.ClientSession() as session:
        urls = ['https://docs.python.org/3/library/asyncio-task.html',
                'https://en.wikipedia.org/wiki/Persian_language',
                'https://en.wikipedia.org/wiki/Persian_Gulf',
                'https://en.wikipedia.org/wiki/ljjllj'
                ]
        rqs = [show_status(session, url) for url in urls]
        status_code = await asyncio.gather(*rqs, return_exceptions=True)
        print(f"status is {status_code}")


asyncio.run(main())
asyncio.run(main_tow())
