# 下载css  确定woff文件名
# import requests
#
#
# headers = {
#     "accept": "text/css,*/*;q=0.1",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "cache-control": "no-cache",
#     "pragma": "no-cache",
#     "priority": "u=0",
#     "referer": "https://www.python-spider.com/challenge/12",
#     "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "style",
#     "sec-fetch-mode": "no-cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
# }
# cookies = {
#     "sessionid": "g9p46xvaj1rxdjt3cg32iz5rnurgy8a5",
#     "no-alert": "true"
# }
# url = "https://www.python-spider.com/static/boke/css/font-awesome.css"
# response = requests.get(url, headers=headers, cookies=cookies)
#
# with open('css/font-awesome.css', 'wb') as f:
#     f.write(response.content)
#


# 下载woff文件
# import requests
#
#
# headers = {
#     "accept": "*/*",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "cache-control": "no-cache",
#     "origin": "https://www.python-spider.com",
#     "pragma": "no-cache",
#     "priority": "u=0",
#     "referer": "https://www.python-spider.com/challenge/12",
#     "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "font",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
# }
# cookies = {
#     "sessionid": "g9p46xvaj1rxdjt3cg32iz5rnurgy8a5",
#     "no-alert": "true"
# }
# url = "https://www.python-spider.com/static/font/challenge12/aiding.woff"
# response = requests.get(url, headers=headers, cookies=cookies)
#
# with open("./woff/aiding.woff", "wb") as f:
#     f.write(response.content)




# 将文件解析成sgv文件并手动确定map
# from fontTools.ttLib import TTFont
# from fontTools.pens.svgPathPen import SVGPathPen
# from xml.dom.minidom import Document
# from pathlib import Path
#
# # 加载字体
# font = TTFont("woff/aiding.woff")
# glyph_set = font.getGlyphSet()
#
# # 输出目录
# Path("glyphs").mkdir(exist_ok=True)
#
# for glyph_name in glyph_set.keys():
#     if glyph_name == ".notdef":
#         continue
#     pen = SVGPathPen(glyph_set)
#     glyph_set[glyph_name].draw(pen)
#     path_data = pen.getCommands()
#
#     # 生成 svg 文件
#     doc = Document()
#     svg = doc.createElement("svg")
#     svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
#     svg.setAttribute("viewBox", "0 0 1000 1000")
#     path = doc.createElement("path")
#     path.setAttribute("d", path_data)
#     svg.appendChild(path)
#     doc.appendChild(svg)
#
#     with open(f"glyphs/{glyph_name}.svg", "w", encoding="utf-8") as f:
#         f.write(doc.toprettyxml())



import asyncio
import aiohttp
import re

# 映射表
mapping = {
    "unif712": 0,
    "unif375": 2,
    "unif295": 6,
    "unif80c": 3,
    "unif12f": 4,
    "unif0d6": 8,
    "uniee4a": 5,
    "unie458": 1,
    "unie449": 7,
    "unie44d": 9
}

# 解码函数
def decode_text(text: str) -> str:
    def repl(m):
        hex_code = m.group(1).lower()   # e449
        glyph = "uni" + hex_code
        return str(mapping.get(glyph, "?"))
    return re.sub(r"&#x([0-9a-fA-F]+);?", repl, text)

# 计算任务
async def fetch_page(session: aiohttp.ClientSession, page: int, lock: asyncio.Lock, sum_holder: dict):
    url = "https://www.python-spider.com/api/challenge12"
    data = {"page": str(page)}

    try:
        async with session.post(url, data=data) as resp:
            res = await resp.json()
            total = 0
            for item in res.get("data", []):
                num_str = decode_text(item["value"]).replace(" ", "")
                if num_str.isdigit():
                    total += int(num_str)
            async with lock:
                sum_holder["sum"] += total
            print(f"Page {page} done, page_sum={total}")
    except Exception as e:
        print(f"Page {page} failed: {e}")

# 主程序
async def main():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "referer": "https://www.python-spider.com/challenge/12",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "sessionid": "g9p46xvaj1rxdjt3cg32iz5rnurgy8a5",
        "no-alert": "true"
    }

    sum_holder = {"sum": 0}
    lock = asyncio.Lock()

    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        tasks = [fetch_page(session, i, lock, sum_holder) for i in range(1, 101)]
        await asyncio.gather(*tasks)

    print("最终总和：", sum_holder["sum"])


if __name__ == "__main__":
    asyncio.run(main())
