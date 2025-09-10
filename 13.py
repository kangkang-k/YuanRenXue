import re
from fontTools.ttLib import TTFont
import asyncio
import aiohttp
import base64

def decode_font_data(data, debug=False):
    woff_bytes = base64.b64decode(data['woff'])
    woff_path = "woff/temp.woff"
    with open(woff_path, "wb") as f:
        f.write(woff_bytes)

    font = TTFont(woff_path)
    cmap = font.getBestCmap()

    glyph_map = {}
    for uni, name in cmap.items():
        if debug:
            print(uni, name)
        if name.startswith("uni"):
            glyph_map[uni] = name[-1]

    def decode_value(val):
        codes = re.findall(r'&#x([0-9a-fA-F]+);?', val)
        return "".join(glyph_map.get(int(code, 16), "?") for code in codes)

    decoded_list = []
    for item in data['data']:
        decoded_list.append({
            **item,
            "value": decode_value(item['value'])
        })

    return decoded_list

url = 'https://www.python-spider.com/api/challenge13'

sum_num = 0
lock = asyncio.Lock()

async def req(session, page):
    global sum_num
    async with session.post(url, data={'page': str(page)}) as response:
        print(await response.text())
        result = await response.json()
        result = decode_font_data(result)
        total = sum(int(j['value'].strip()) for j in result)
        async with lock:
            sum_num += total
        print(f'第{page}页计算完成')

async def main():
    async with aiohttp.ClientSession() as session:
        pages = list(range(1, 101))
        batch_size = 5
        for i in range(0, len(pages), batch_size):
            batch = pages[i:i+batch_size]
            tasks = [asyncio.create_task(req(session, page)) for page in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # 每批请求间隔 2 秒，可调

if __name__ == '__main__':
    asyncio.run(main())
    print('最终的结果是:', sum_num)
