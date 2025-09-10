import asyncio
import aiohttp
import execjs
url = 'https://www.python-spider.com/api/challenge58'

sum_num = 0
lock = asyncio.Lock()

with open('js/58.js', 'r', encoding='utf-8') as f:
    content = f.read()
    jscode = execjs.compile(content)


async def req(session, page):
    global sum_num

    async with session.post(url, data={'page': str(page),
                                       "token": jscode.call('md5',str(page))}) as response:
        result = await response.json()
        print(result)
        total = sum(int(j['value'].strip()) for j in result['data'])
        async with lock:
            sum_num += total
        print(f'第{page}页计算完成')


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(req(session, i)) for i in range(1, 101)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    print('最终的结果是:', sum_num)
