import asyncio
import aiohttp
import base64
import time
import hashlib
url = 'https://www.python-spider.com/api/challenge57'

sum_num = 0
lock = asyncio.Lock()


async def req(session, page):
    global sum_num

    async with session.post(url, data={'page': page}) as response:
        print(await response.text())
        # result = await response.json()
        # total = sum(int(j['value'].strip()) for j in result['data'])
        # async with lock:
        #     sum_num += total
        # print(f'第{page}页计算完成')


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(req(session, i)) for i in range(1, 101)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    print('最终的结果是:', sum_num)