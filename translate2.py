from urllib import request, parse
import time
import random
import hashlib
import json
import requests

def get_ts(): #时间戳 乘以1000 取整  
    ts = str(int(1000 * time.time()))
    return ts


def get_salt(ts):
    salt = ts + str(random.randint(0, 10)) # 上面的方法返回值 加上1-10之间的随机数  
    return salt


def get_sign(words, salt):
    content = 'fanyideskweb' + words + salt + 'n%A-rKaT5fb[Gy?;N5@Tj'
    sign = hashlib.md5(content.encode()).hexdigest()
    return sign


def translate(words, ts, salt, sign):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    data = {
        "i": words,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        'ts': ts,
        'bv': 'bbb3ed55971873051bc2ff740579bb49',
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTIME",
        "typoResult": "false"
    }

    data = parse.urlencode(data).encode()

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': len(data),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__guid=204659719.2422785200799945700.1554675512727.244; OUTFOX_SEARCH_USER_ID=-1327275086@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=378292303.3354687; JSESSIONID=aaaLYwaICIOxi6ofRh8Nw; monitor_count=8; ___rl__test__cookies=1554693830913',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    req = request.Request(url=url, data=data, headers=headers)
    
    rsp = request.urlopen(req)
    print(rsp.getcode())
    html = rsp.read().decode('utf-8')
    json_data = json.loads(html)
    print(json_data)
    print('翻译的结果为：' + json_data['translateResult'][0][0]['tgt'])


if __name__ == '__main__':
    words = input('请输入要翻译的内容：')
    ts = get_ts()
    salt = get_salt(ts)
    sign = get_sign(words, salt)
    translate(words, ts, salt, sign)