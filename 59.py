# import requests
#
#
# headers = {
#     "accept": "application/json, text/javascript, */*; q=0.01",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "cache-control": "no-cache",
#     "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "origin": "https://www.python-spider.com",
#     "pragma": "no-cache",
#     "priority": "u=1, i",
#     "referer": "https://www.python-spider.com/challenge/59",
#     "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
#     "x-requested-with": "XMLHttpRequest"
# }
# cookies = {
#     "sessionid": "g9p46xvaj1rxdjt3cg32iz5rnurgy8a5",
#     "no-alert": "true"
# }
# url = "https://www.python-spider.com/api/challenge59"
# data = {
#     "page": "4"
# }
# response = requests.post(url, headers=headers, cookies=cookies, data=data)
#
# print(response.text)
# print(response)


import asyncio
import aiohttp

url = 'https://www.python-spider.com/api/challenge59'

sum_num = 0
lock = asyncio.Lock()


async def req(session, page):
    global sum_num
    async with session.post(url, data={'page': str(page)}) as response:
        result = await response.json()
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