
# -*- coding:utf-8 -*-
import os
import argparse
import dbm
import requests
from urllib import request, parse
import re
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process
import time
import random
import hashlib
import json


class Bing(object):

    def __init__(self):
        super(Bing, self).__init__()

    def query(self, word):
        from bs4 import BeautifulSoup
        sess = requests.Session()
        headers = {
            'Host': 'cn.bing.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
        }
        sess.headers.update(headers)
        url = 'http://cn.bing.com/dict/SerpHoverTrans?q=%s' % (word)
        try:
            resp = sess.get(url, timeout=100)
        except:
            return None
        text = resp.text
        if (resp.status_code == 200) and (text):
            soup = BeautifulSoup(text, 'lxml')
            if soup.find('h4').text.strip() != word:
                return None
            lis = soup.find_all('li')
            trans = []
            for item in lis:
                transText = item.get_text()
                if transText:
                    trans.append(transText)
            return '\n'.join(trans)
        else:
            return None


class Youdao(object):

    def __init__(self):
        super(Youdao, self).__init__()

    def query(self, word):
        ts = str(int(1000 * time.time()))
        salt = ts + str(random.randint(0, 10))
        content = 'fanyideskweb' + word + salt + 'n%A-rKaT5fb[Gy?;N5@Tj'
        sign = hashlib.md5(content.encode()).hexdigest()
        url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

        data = {
            "i": word,
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

        try:
            req = request.Request(url=url, data=data, headers=headers)
            rsp = request.urlopen(req)
        except:
            return None
        html = rsp.read().decode('utf-8')
        json_data = json.loads(html)
        if (rsp.getcode() == 200) and (json_data):
            transs=json_data['translateResult'][0][0]['tgt']
            # print(transs)
            trans = []
            trans.append(transs)
            
            return '\n'.join(trans)
        else:
            return None


class Iciba(object):

    def __init__(self):
        super(Iciba, self).__init__()

    def query(self, word):
        from bs4 import BeautifulSoup
        sess = requests.Session()
        headers = {
            'Host': 'open.iciba.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate'
        }
        sess.headers.update(headers)
        url = 'http://open.iciba.com/huaci_new/dict.php?word=%s' % (word)
        try:
            resp = sess.get(url, timeout=100)
            text = resp.text
            pattern = r'(<div class=\\\"icIBahyI-group_pos\\\">[\s\S]+?</div>)'
            text = re.search(pattern, text).group(1)
        except:
            return None
        if (resp.status_code == 200) and (text):
            soup = BeautifulSoup(text, 'lxml')
            ps = soup.find_all('p')
            trans = []
            for item in ps:
                transText = item.get_text()
                transText = re.sub(
                    r'\s+', ' ', transText.replace('\t', '')).strip()
                if transText:
                    trans.append(transText)
            return '\n'.join(trans)
        else:
            return None


path = os.path.dirname(os.path.realpath(__file__))
db={}
# db = dbm.open(path + '/data/vocabulary', 'c')
DEFAULT_SERVICE = 'youdao'


class Client(object):

    def __init__(self, word, service=None, webonly=False):
        super(Client, self).__init__()
        if not service:
            service = DEFAULT_SERVICE
        self.service = service
        self.word = word
        self.trans = None
        if webonly:
            self.db = {}
        else:
            self.db = db

    def translate(self):
        trans = self.db.get(self.word)
        if trans:
            return trans
        else:
            if self.service == 'bing':
                S = Bing()
            if self.service == 'youdao':
                S = Youdao()
            elif self.service == 'iciba':
                S = Iciba()
            trans = S.query(self.word)
            self.trans = trans
            return trans

    def suggest(self):
        if re.sub(r'[a-zA-Z\d\'\-\.\s]', '', self.word):
            return None
        import enchant
        try:
            d = enchant.DictWithPWL(
                'en_US', path + '/data/spell-checker/american-english-large')
        except:
            d = enchant.Dict('en_US')
        suggestion = d.suggest(self.word)
        return suggestion

    def hyphenate(self):
        sess = requests.Session()
        url = 'http://dict.cn/%s' % (self.word)
        hyphenation = None
        try:
            resp = sess.get(url, allow_redirects=False, timeout=100)
            # pattern = ur'<h1 class="keyword" tip="音节划分：([^"]+)">'
            # hyphenation = re.search(pattern, resp.text).group(1).replace('&#183;', '-')
            hyphenation = resp.text
        except:
            pass
        return hyphenation

    def pronounce(self, tts):
        if tts == 'festival':
            cmd = ' echo "%s" | festival --tts > /dev/null 2>&1' % (self.word)
        elif tts == 'espeak':
            cmd = 'espeak -v en-us "%s" > /dev/null 2>&1' % (self.word)
        elif tts == 'real':
            cmd = 'find %s/data/RealPeopleTTS/ -type f -iname "%s.wav" | head -n1 | xargs -I {} aplay {} > /dev/null 2>&1' % (
                path, self.word)
        import commands
        try:
            status, output = commands.getstatusoutput(cmd)
        except:
            pass
        return True

    def updateDB(self):
        if self.trans:
            db[self.word] = self.trans.encode('utf-8')
        # db.close()
        return True


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('word', help="word or 'some phrase'")
    parser.add_argument('-n', '--nostorage', dest='nostorage',
                        action='store_true', help='turn off data storage')
    parser.add_argument('-p', '--pronounce', dest='pronounce', choices=[
                        'espeak', 'festival', 'real'], help="text-to-speech software: 'espeak', 'festival' or 'real'")
    parser.add_argument('-s', '--service', dest='service', choices=[
                        'bing', 'youdao', 'iciba'], help="translate service: 'bing', 'youdao' or 'iciba'")
    parser.add_argument('-w', '--webonly', dest='webonly',
                        action='store_true', help='ignore local data')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.1.4')
    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    word = args.word.strip()
    service = args.service
    webonly = args.webonly
    if service:
        webonly = True
    C = Client(word, service=service, webonly=webonly)
    pool = ThreadPool()
    _hyphen = pool.apply_async(C.hyphenate)
    _trans = pool.apply_async(C.translate)
    _suggestion = pool.apply_async(C.suggest)
    hyphen = _hyphen.get()
    trans = _trans.get()
    if trans:
        if hyphen:
            # print(hyphen)
            print(word,"的翻译结果是:")
        print(trans)
        if args.pronounce:
            p1 = Process(target=C.pronounce, args=(args.pronounce,))
            p1.daemon = True
            p1.start()
        if not args.nostorage:
            p2 = Process(target=C.updateDB)
            p2.daemon = True
            p2.start()
    else:
        suggestion = _suggestion.get()
        if not suggestion:
            print('No translations found for \"%s\" .' % (word))
        else:
            print('No translations found for \"%s\", maybe you meant:\
                  \n\n%s' % (word, ' / '.join(suggestion)))
