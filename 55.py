import asyncio
import base64
import json
import aiohttp
from Crypto.Cipher import AES
url = 'https://www.python-spider.com/api/challenge55'

sum_num = 0
lock = asyncio.Lock()


def decode(str_cipher):
    KEY = b'aiding6666666666'
    cipher = AES.new(KEY, AES.MODE_ECB)

    decoded_bytes = base64.b64decode(str_cipher)

    decrypted_bytes = cipher.decrypt(decoded_bytes)

    pad_len = decrypted_bytes[-1]
    decrypted_bytes = decrypted_bytes[:-pad_len]

    return decrypted_bytes.decode('utf-8')

async def req(session, page):
    global sum_num

    async with session.post(url, data={'page': str(page)}) as response:
        result = await response.json()
        datas = json.loads(decode(result['result']))
        total = sum(int(j['value'].strip()) for j in datas['data'])
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