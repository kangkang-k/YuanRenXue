import asyncio
import aiohttp

url = 'https://www.python-spider.com/api/challenge7'

sum_num = 0
lock = asyncio.Lock()


async def pre_req(session):
    city_url = 'https://www.python-spider.com/cityjson'
    async with session.post(city_url) as response:
        await response.read()


async def req(session, page):
    global sum_num

    await pre_req(session)
    async with session.post(url, data={'page': str(page)}) as response:
        result = await response.json()
        total = sum(int(j['value'].strip()) for j in result['data'])
        async with lock:
            sum_num += total
        print(f'第{page}页计算完成')


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 101):
            tasks.append(asyncio.create_task(req(session, i)))
            if i % 4 == 0:
                await asyncio.sleep(1)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    print('最终的结果是:', sum_num)
