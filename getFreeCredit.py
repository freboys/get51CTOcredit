import requests
from lxml import etree
import sys
import time
import random


def read_txt(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    return lines


for line in read_txt('userPass.txt'):
    username = line.split(' ')[0].strip()
    password = line.split(' ')[1].strip()
    ua_pool = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    ]

    headers = {'User-Agent': random.choice(ua_pool)}
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9'

    index_url = 'http://home.51cto.com/index'
    home_url = 'http://home.51cto.com/home'

    client = requests.Session()
    resp = client.get(index_url, headers=headers)
    # 获取_csrf
    selector = etree.HTML(resp.text)
    csrf = selector.xpath('//*[@id="login-form"]/input[@name="_csrf"]/@value')[0]
    print(csrf)
    data = {'_csrf':csrf, 'LoginForm[username]': username, 'LoginForm[password]': password,
            'rememberMe': 0, 'login-button': '登 录'}
    client.post(index_url, data=data, headers=headers)

    # 判断是否登陆成功
    resp_home = client.get(home_url)
    selector_home = etree.HTML(resp_home.text)
    nickname = selector_home.xpath('//div[@id="login_status"]/ul/li[1]/a[1]/text()')
    print(nickname)
    with open('D:/tmp/test6.html', 'wb') as f:
        f.write(resp_home.content)
        f.close()

    # client.get('http://home.51cto.com/space?uid=354649', headers=headers)
    # client.get('http://down.51cto.com/credits', headers=headers)
    # 领取下载豆
    print(username)
    print("开始领取下载豆")
    r = client.get('http://down.51cto.com/download.php?do=getfreecredits', headers=headers)
    print(r.text)
    with open('out.log', 'a') as f:
        f.write(username)
        f.write('\n')
        f.write(r.text)
        f.write('\n')
        f.close()
    time.sleep(3)
    # 领取无忧币
    print("开始领取无忧币")
    r = client.get(home_url, headers=headers)
    selector = etree.HTML(r.text)
    csrf_token = selector.xpath('/html/head/meta[3]/@content')[0]
    data = {'_csrf': csrf_token}
    headers['X-CSRF-Token'] = csrf_token
    headers['Referer'] = home_url
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    r = client.post('http://home.51cto.com/home/ajax-to-sign', data=data, headers=headers)
    print(r.text)
    with open('out.log', 'a') as f:
        f.write(username)
        f.write('\n')
        f.write(r.text)
        f.write('\n')
        f.close()
    time.sleep(3)

    # 领取51CTO学院的学分
    print("开始领取学分")
    score_referer_url = 'http://edu.51cto.com/center/'
    client.get(score_referer_url)
    headers['Referer'] = score_referer_url
    score_url = "http://edu.51cto.com/center/user/index/task"
    resp_score = client.get(score_url, headers=headers)
    print(resp_score.text)



