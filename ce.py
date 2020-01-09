# -*- coding: utf-8 -*-
from urllib import request,parse
import json
import time
from hashlib import md5
'''
def dicToSortedStrParam(dic={}):
  keyList = sorted(dic)
  str =""
  for i,key in enumerate(keyList):
    if i==len(keyList)-1:
      str += key +"="+ dic[key]
    else:
      str += key +"="+ dic[key] + "&"
    pass
  return str
'''
 
 
def create_md5(data):
  md5_obj = md5()
  md5_obj.update(data.encode("utf-8"))
  return md5_obj.hexdigest()
 
if __name__ == "__main__":
  request_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
  translate = "hell"
  c = "fanyideskweb"
  data = {}
  data["i"] = translate
  data["from"] = "AUTO"
  data["to"] = "AUTO"
  data["smartresult"] = "dict"
  data["client"] = c
  data["doctype"] = "json"
  data["version"] = "2.1"
  data["keyfrom"] = "fanyi.web"
  data["action"] = "FY_BY_REALTIME"
  data["typoResult"] = "false"
  salt = str(int(round(time.time(),3)*1000))
  # 加密
  data["salt"] = salt
  # a = "rY0D^0'nM0}g5Mm1z%1G4"  网上别人的 也可以
  a = "ebSeFb%=XZ%T[KZ)c(sy!"
  sign = create_md5(c+translate+salt+a)
  data["sign"] = sign
  headers = {}
  headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
  # headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
  headers["Referer"] = "http://fanyi.youdao.com/"
  # headers["Host"] = "fanyi.youdao.com"
  # headers["Origin"]="http://fanyi.youdao.com"
  headers["Cookie"]="OUTFOX_SEARCH_USER_ID=-948455480@10.169.0.83; " \
           "JSESSIONID=aaajvZPcjhFWbgtIBPuiw; " \
           "OUTFOX_SEARCH_USER_ID_NCOO=1148682548.6241577;" \
           " fanyi-ad-id=41685; fanyi-ad-closed=1; ___rl__test__cookies="+salt
 
  data = parse.urlencode(data).encode('utf-8')
  request1 = request.Request(request_url,data,headers = headers)
 
  response = request.urlopen(request1)
  print(response.info())
  #读取信息并解码
  html = response.read().decode('utf-8')
  print(html)
  #使用JSON
  translate_results = json.loads(html)
  # 找到翻译结果
  translate_results = translate_results['translateResult'][0][0]['tgt']
  # 打印翻译信息
  print("翻译的结果是：%s" % translate_results)