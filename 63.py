import asyncio
import json
import aiohttp
import base64
import execjs

url = 'https://www.python-spider.com/api/challenge63'

sum_num = 0
lock = asyncio.Lock()

with open('js/63.js', 'r', encoding="utf-8") as f:
    js_code = f.read()
js_ctx = execjs.compile(js_code)


async def req(session, page):
    global sum_num
    data = js_ctx.call("get_code", str(page))

    async with session.post(url, data=base64.b64decode(data)) as response:
        raw = await response.read()  # 拿二进制
        decoded = js_ctx.call("decode", base64.b64encode(raw).decode('utf-8'))
        result = json.loads(decoded)

        total = sum(int(j['value'].strip()) for j in result['data'])
        async with lock:
            sum_num += total
        print(f'第{page}页计算完成, 累加 {total}')

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(req(session, i)) for i in range(1, 101)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
    print('最终的结果是:', sum_num)
