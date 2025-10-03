import asyncio
import aiohttp

url = 'https://www.python-spider.com/api/challenge4'

# 隧道代理配置
proxy = "http://6A997D2D:BA2A6867D232@tun-ovhwip.qg.net:18736"

sum_num = 0
lock = asyncio.Lock()

# 限速：每秒最多 5 个请求
semaphore = asyncio.Semaphore(5)


async def req(session, page):
    global sum_num
    async with semaphore:  # 控制并发速率
        try:
            async with session.post(url, data={'page': str(page)}, proxy=proxy, timeout=10) as response:
                result = await response.json()
                total = sum(int(j['value'].strip()) for j in result['data'])
                async with lock:
                    sum_num += total
                print(f'第{page}页完成')
        except Exception as e:
            print(f"第{page}页请求失败: {e}")
        await asyncio.sleep(1)  # 保证速率不超过 5/s


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(req(session, i)) for i in range(1, 101)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    print('最终结果:', sum_num)



# todo 需要高质量ip代理，此代码换上高质量代理 理论能通过
