import asyncio
import execjs
import aiohttp

with open('js/3.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
js_comp = execjs.compile(js_code)
url = 'https://www.python-spider.com/api/challenge3'
CONCURRENCY = 10

async def get_m(loop):
    return await loop.run_in_executor(None, js_comp.call, 'get_m')

async def fetch(session, page, sem, loop):
    async with sem:
        m = await get_m(loop)
        cookies = {'m': m}
        data = {'page': page}
        async with session.post(url, data=data, cookies=cookies, timeout=30) as resp:
            j = await resp.json()
            items = j.get('data', [])
            return sum(int(x['value']) for x in items)

async def main():
    sem = asyncio.Semaphore(CONCURRENCY)
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, i, sem, loop) for i in range(1, 101)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    total = 0
    for r in results:
        if isinstance(r, Exception):
            # 出错的页可以重试或记录，这里忽略
            continue
        total += r
    print(total)

if __name__ == '__main__':
    asyncio.run(main())
