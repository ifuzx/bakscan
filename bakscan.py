#--coding:UTF-8--
import base64
import getopt
import os
import json
import re
import sys
import urllib
from urllib import request
import bakthread
import requests

banner = '''
 _         _         _              _   
| |_  ___ | |__ ___ | |_  ___  ___ | |__
| . \<_> || / // | '| . |/ ._>/ | '| / /
|___/<___||_\_\\_|_.|_|_|\___.\_|_.|_\_\\n
                            author:mfsva    v 1.2

please input email，key 

example:
    python3 bakscan.py -s 'body="thinkphp" && after="2021-01-01"'
'''

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
search = ''

def getParam(argv):
    try:
        opts, args = getopt.getopt(argv, "s:", ["ifile="])
    except getopt.GetoptError:
        print('bakscan.py -s <search>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(banner)
            sys.exit()
        elif opt in ("-s", "--Fofa 查询参数"):
            search= arg
            # print(search)
            return search

def FofaSearch(name,size):
    size=str(size)
    email = ""
    key = ""
    b64 =base64.b64encode(name.encode('UTF-8'))
    url="https://fofa.so/api/v1/search/all?email="+email+"&key="+key+"&size="+size+"&qbase64="+str(b64).replace("b'",'').replace("'",'').replace('=','%3D')
    # print(url)
    request = urllib.request.Request(url, headers=headers)
    req = urllib.request.urlopen(request).read()
    req = json.loads(req)
    return req


def alive_cc(name):

    return

def bakfilescan():
    bakthread.run()
    return


def setagreement(name):
    if re.match(r'http', name):
        return (name+"\n")
    else:
        return ("http://" + name+"\n"+"https://" + name+"\n")
    # bakfilescan(n[0])

if __name__ == '__main__':

    # parameter =
    print(banner)
    search=getParam(sys.argv[1:])
    # print(search)
    size = 10000
    if os.path.exists("runoob.txt"):
        os.remove("runoob.txt")
    fo = open("runoob.txt", "w+")
    try:
        info = FofaSearch(search,size)
        # print(info)
        search_id = info['query']
        search_size= str(info['size'])
        search_results = info['results']
        for n in search_results:
            fo.seek(0, 2)
            fo.write(setagreement(n[0]))
        fo.close()
        print("查询参数："+search_id)
        print("查询条数：" + search_size )
        print("文件runoob.txt写入成功")
    except BaseException :
        sys.exit()
    bakfilescan()
