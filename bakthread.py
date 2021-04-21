import re
import requests
import threading
import queue as Queue
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        while True:
            try:
                bakburp(self.name, self.q)
            except:
                break

def bakburp(threadName, q):
    geturl = q.get(timeout=10)
    html=""
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        conn = requests.get(geturl,verify=False, allow_redirects=False,timeout=30)
        conn.encoding = 'utf-8'
        html = conn.status_code
        s = requests.session()
        if html == 200:
            err = len(conn.content)
            if err < 1000000:
                print('\r'+f'\033[33m[*]\033[33mCode：%s -----（可能误报)--大小：%s  ----- 目标：%s  \n' % (html,err,geturl),end='', flush=True)
            else:
                print('\r'+f'\033[32m[*]\033[32m Code：%s ----- 文件存在--大小：%s  ----- 目标：%s  \n' % (html, err, geturl), end='',flush=True)
            # print('Code：%s ----- 文件存在--大小：%s ----- 目标：%s' % (html, err, geturl) )
            s.close()
            conn.close()
        else:
            print('\r'+geturl+'\r',end='', flush=True)
            s.close()
            conn.close()
    except Exception as e:
        print('\r'+geturl+'\r',end='', flush=True)

def run():
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    inurl = {"/www.zip", "/www.rar", "/www.tar.gz", "/wwwroot.zip", "/wwwroot.rar", "/wwwroot.tar.gz", "/web.zip",
                 "/web.rar", "/web.tar.gz", "/.svn" , "/.git" , "/.DS_Store", "/1.zip", "/1.rar","/1.rar" }
    hz = {".zip", ".rar", ".tar.gz"}
    threadLock = threading.Lock()

    link_list = open(r'./runoob.txt', 'r').readlines()
    newlink_list =[]
    data = []

    for i in link_list:
        i=i.replace("\n","")
        for s in inurl:
            url = i + s
            newlink_list.append(url)
        compile_rule = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        # if re.compile(r'\d+[\.]\d+[\.]\d+[\.]\d+'，)
        if re.findall(compile_rule, i):
            continue

        if i.startswith("https://"):
            ex_domain = i.replace("https://", "").split('.')
            # print(ex_domain)
            for index in hz:
                url = i +'/' + i.replace("https://", "") + index
                newlink_list.append(url)
            for top in ex_domain:
                for end in hz:
                    url = i + '/' + top + end
                    newlink_list.append(url)
        elif i.startswith("http://"):
            ex_domain = i.replace("http://", "").split('.')
            for index in hz:
                url = i + '/' + i.replace("http://", "") + index
                newlink_list.append(url)
            for top in ex_domain:
                for end in hz:
                    url = i + '/'+ top+end
                    newlink_list.append(url)
    # for i in newlink_list:
    #     print(i)
    # 创建50个线程名
    thnum = 100
    threadList = []
    num=0
    while num <= thnum:
        threadList.append("thread" + str(num))
        num+=1
    # 设置队列长度
    workQueue = Queue.Queue(3000)
    # 线程池# 创建新线程
    threads = []
    for tName in threadList:
        thread = myThread(tName, workQueue)
        thread.start()
        # threadLock.acquire()
        # threadLock.release()
        threads.append(thread)
    # 将url填充到队列
    for url in newlink_list:
        workQueue.put(url)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("end")
