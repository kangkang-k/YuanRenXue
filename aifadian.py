import aiofiles
import asyncio
import aiohttp
import time
import os


async def get_album(session):
    url = 'https://afdian.com/api/user/get-album-list?user_id=cac601d6379e11ecb98e52540025c377&page=1&per_page=10'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "afd-fe-version": "20250605",
        "afd-stat-id": "128ad7b4992311f094a052540025c377",
        "cache-control": "no-cache",
        "locale-lang": "zh-CN",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://afdian.com/a/yezi233?tab=feed",
        "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
    }
    cookies = {
        "auth_token": "d91e2d2120f59e05cef430c1510225a0_20250924164736",
        "_gid": "GA1.2.2056224506.1758903649",
        "_ga": "GA1.1.2127832341.1758703639",
        "_ga_6STWKR7T9E": "GS2.1.s1758903649$o3$g1$t1758906816$j54$l0$h1743402328",
        "_ga_ZF21E9SBHP": "GS2.1.s1758903649$o3$g1$t1758906816$j54$l0$h1471167913"
    }
    async with session.get(url, headers=headers, cookies=cookies) as resp:
        data = await resp.json()
        # 返回 album_id: post_count dict
        return {i['album_id']: i['post_count'] for i in data['data']['list']}


async def get_url(session, album_id, rank):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "afd-fe-version": "20250605",
        "afd-stat-id": "128ad7b4992311f094a052540025c377",
        "cache-control": "no-cache",
        "locale-lang": "zh-CN",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": f"https://afdian.com/album/{album_id}",
        "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
    }
    cookies = {
        "auth_token": "d91e2d2120f59e05cef430c1510225a0_20250924164736",
        "_gid": "GA1.2.2056224506.1758903649",
        "_ga": "GA1.1.2127832341.1758703639",
        "_ga_6STWKR7T9E": "GS2.1.s1758903649$o3$g1$t1758905465$j60$l0$h1743402328",
        "_ga_ZF21E9SBHP": "GS2.1.s1758903649$o3$g1$t1758905465$j60$l0$h1471167913"
    }
    url = f'https://afdian.com/api/user/get-album-post?album_id={album_id}&lastRank={rank}&rankOrder=asc&rankField=rank'
    async with session.get(url, headers=headers, cookies=cookies) as resp:
        return await resp.json()


async def download_video(session, title, url):
    print(f'开始下载：{title}')
    filepath = f'video/{title}.mp4'
    if os.path.exists(filepath):
        print(f'已跳过已存在视频：{title}')
        return
    async with session.get(url) as resp:
        content = await resp.read()
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(content)
        print(f'已下载：{title}')


async def run():
    os.makedirs('video', exist_ok=True)
    async with aiohttp.ClientSession() as session:
        album_dict = await get_album(session)
        for album_id, post_count in album_dict.items():
            print(f'开始下载此id下的视频:{album_id},预计{post_count}个')
            for rank in range(0, post_count, 10):
                data = await get_url(session, album_id, rank)
                for i in data['data']['list']:
                    if not i.get('video'):
                        continue
                    title = i['title']
                    url = i['video']
                    await download_video(session, title, url)


def main_with_retry():
    while True:
        try:
            asyncio.run(run())
            break  # 成功完成则退出循环
        except Exception as e:
            print(f"发生错误: {e}，3秒后重试...")
            time.sleep(3)  # 等待后重试


if __name__ == '__main__':
    main_with_retry()
