import asyncio
import aiohttp


async def show_status(session, url):
    async with session.get(url) as result:
        return f'status for {url} is {result.status}'


async def main():
    async with aiohttp.ClientSession() as session:
        requests = [asyncio.create_task(show_status(session, 'https://docs.python.org/3/library/asyncio-task.html')),
                    asyncio.create_task(show_status(session, 'https://en.wikipedia.org/wiki/Persian_language')),
                    asyncio.create_task(show_status(session, 'https://en.wikipedia.org/wiki/Persian_Gulf')),
                    asyncio.create_task(show_status(session, 'https://en.gkkk.org/'))
                    ]
        done, pending = await asyncio.wait(requests, return_when=asyncio.FIRST_COMPLETED)
        print(f'done ===> {done}')
        print(f'pending ===> {pending}')
        for dn in done:
            if dn.exception() is None:
                print(dn.result())
            else:
                print("Error")
        for pd in pending:
            pd.cancel()
        print(f'after cancel {pending}')
asyncio.run(main())
