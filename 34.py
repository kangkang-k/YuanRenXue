import requests


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "priority": "u=0, i",
    "referer": "https://www.python-spider.com/challenge/34",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": "3jjrdljluer2dvdjckxxt35r5e139xzc",
    "no-alert": "true",
    "yuanrenxue34": "cMedwOsHVo",
    "iloveu": "4b39c30ea77b495182946f2ebbd5ac03f9180914"
}
url = "https://www.python-spider.com/challenge/34"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
print(response)