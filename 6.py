import  requests


headers={
    "Host": "www.python-spider.com",
    'Content-Length':'6',
    "Connection": "keep-alive",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.python-spider.com/challenge/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

cookies={

    "sessionid": "g9p46xvaj1rxdjt3cg32iz5rnurgy8a5",
    "sign": "tlvwhirqfp"
}

url='https://www.python-spider.com/api/challenge6'
session = requests.Session()
values=[]

session.headers.clear()
session.headers.update(headers)

for p in range(1,101):
    data = {
        'page': p
    }

    headers['Content-Length'] = str(len("page={}".format(p)))
    print(headers)
    print(data)


    if p >2:
        cookies=session.cookies.get_dict()
    response = session.post(url, headers=headers, cookies=cookies, data=data)#,proxies=proxies, verify=False)
    print("返回r",response.headers['Set-Cookie'])
    # 查看所有cookies
    print("所有Cookies:")
    print(session.cookies.get_dict())
    if response.status_code==200:

        print(response.json())
        for item in response.json()["data"]:
            if isinstance(item["value"],int):
                values.append(item["value"])
            else:
                values.append(int(item["value"].strip("\r")))
print(sum(values))