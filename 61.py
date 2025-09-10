import asyncio
import websockets
import execjs

WS_URL = "wss://www.python-spider.com/api/challenge61"

with open('js/61.js', 'r', encoding='utf-8') as f:
    code = f.read()
    js_code = execjs.compile(code)

async def send_and_receive(page: int):
    async with websockets.connect(WS_URL) as ws:
        message = js_code.call("get_msg", page)
        await ws.send(message)
        print(f"发送: {message}")
        response = await ws.recv()
        print(f"接收: {response}")

async def main():
    # 一次性发 100 页
    tasks = [send_and_receive(i) for i in range(1, 101)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # 🚀 先测试单页
    asyncio.run(send_and_receive(3))

    # 🚀 确认没问题后，再跑全量
    # asyncio.run(main())
