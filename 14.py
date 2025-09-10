import execjs
import asyncio
import aiohttp

url = 'https://www.python-spider.com/api/challenge14'

sum_num = 0
lock = asyncio.Lock()
with open('js/14.js','r',encoding='utf-8') as f:
    content = f.read()
    js_code = execjs.compile(content)

print(js_code.call('get_uc', 2))

async def req(session, page):
    global sum_num
    async with session.post(url, data={'page': str(page), 'uc': js_code.call('get_uc', page)}) as response:
        result = await response.json()
        total = sum(int(j['value'].strip()) for j in result['data'])
        async with lock:
            sum_num += total
        print(f'第{page}页计算完成')

async def main():
    async with aiohttp.ClientSession() as session:
        for i in range(1, 101, 10):  # 每批10页
            tasks = [asyncio.create_task(req(session, j)) for j in range(i, min(i + 10, 101))]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # 每10页休眠1秒

if __name__ == '__main__':
    asyncio.run(main())
    print('最终的结果是:', sum_num)
