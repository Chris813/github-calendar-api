# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler,HTTPServer
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
def getdata(name):
    print(name)
    gitpage = requests.get("https://github.com/" + name,proxies={
        # "http": "http://127.0.0.1:7890",
        # "https": "http://127.0.0.1:7890",
    })
    print(gitpage)
    
    data = gitpage.text
    datadatereg = re.compile(r'data-date="(.*?)" data-level')
    datacountreg = re.compile(r'<span class="sr-only">(.*?) contribution')
    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    datacount = list(map(int, [0 if i == "No" else i for i in datacount]))

    # 将datadate和datacount按照字典序排序
    sorted_data = sorted(zip(datadate, datacount))
    datadate, datacount = zip(*sorted_data)
    
    contributions = sum(datacount)
    datalist = []
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path == '/favicon.ico':
            # 处理 /favicon.ico 请求
            self.send_response(200)
            self.end_headers()
            return
        else:
            print(f'GET {path}')
            user = path.split('?')[1]
            data = getdata(user)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

