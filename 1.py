# import asyncio
# import aiohttp
# import base64
# import time
# import hashlib
# url = 'https://www.python-spider.com/api/challenge1'
#
# sum_num = 0
# lock = asyncio.Lock()
#
#
# async def req(session, page):
#     global sum_num
#     a = '9622'
#     timestamp = str(int(time.time()))
#     tokens = hashlib.md5(base64.b64encode((a + timestamp).encode())).hexdigest()
#     headers = {
#         "safe":tokens,
#        "Timestamp":timestamp
#    }
#     async with session.post(url, data={'page': str(page)},headers = headers) as response:
#         result = await response.json()
#         total = sum(int(j['value'].strip()) for j in result['data'])
#         async with lock:
#             sum_num += total
#         print(f'第{page}页计算完成')
#
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.create_task(req(session, i)) for i in range(1, 101)]
#         await asyncio.gather(*tasks)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
#     print('最终的结果是:', sum_num)





# RPC远程调用测试：
# 浏览器端ws服务代码：
# let ws = new WebSocket("ws://localhost:8765");
#
# ws.onmessage = async (event) => {
#   let data = JSON.parse(event.data);
#   try {
#     let result = eval(data.code);  // 执行传来的 JS
#     ws.send(result === undefined ? "undefined" : JSON.stringify(result));
#   } catch (e) {
#     ws.send("error: " + e.message);
#   }
# };

# python ws代码：
import asyncio
import websockets
import json

async def handler(ws):
    while True:
        code = input("输入要执行的JS: ")
        await ws.send(json.dumps({"code": code}))
        result = await ws.recv()
        print("返回:", result)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
