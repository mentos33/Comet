#!/usr/bin/env python
#coding=utf-8
import argparse
import logging
import requests
from urlparse import urlparse
import os
import json
from Spider.dynamic import link
from Scanner.xss import xss
from Scanner import sql
'''
comet 的入口

'''


payloads = ['<svg "ons>', '" onfocus="alert(1);', 'javascript:alert(1)', '"><svg/onload=alert`1`>']

blacklist = ['.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.avi', '.gif', '.svg',
             '.pdf']


xss_conf = 'xss_conf.json'

headers = {'User_Agent':"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}

class color:
    BLUE = '\033[94m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def log(lvl, col, msg):
        logger.log(lvl, col + msg + color.END)


logger = logging.getLogger(__name__)#实例化
logger.setLevel(logging.DEBUG)#日志输出的等级

lh = logging.StreamHandler()  # Handler for the logger  加控制台输出流处理器
#lh.setlevel(logging.INFO)
logger.addHandler(lh)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%Y %b %d, %H:%M:%S')#设置输出格式
lh.setFormatter(formatter)


#交互 接受参数  ''https:// 
parser = argparse.ArgumentParser()
parser.add_argument('-u', dest='url', help='URL of Target Website')
parser.add_argument('-c', dest='cookies', help='add cookies')
parser.add_argument('-e', action='store_true', dest='compOn',help='Enable comprehensive scan')
parser.add_argument("-t", dest="target", help="scan target website", metavar="www.example.com")

results = parser.parse_args()

def singlescan(url):
    "scan single targeted domain"

    if urlparse(url).query != '':
        result = sql.scan(url)
        if result != []:
            return result
        else:
            print ("no SQL injection vulnerability found")
    else:
        print ('please input url with params')
    return False
if results.url and results.target:
    parser.print_help()
    os._exit(0)
elif results.url:
    format_url = check_url(results.url)
    if results.cookies:
        print ('use cookies :{0}'.format(results.cookies))
    mylink = link(format_url)
    count = 0
    alllinks = []
    if results.compOn:
        print ('Doing a comprehensive traversal')
        alllinks = mylink.get_all_links()
    else:
        alllinks = mylink.get_links()
    with open('url_list.txt','w') as f:
        for _ in alllinks:
            f.write(_+"\n")
    print 'num of links : '+str(len(alllinks))
    if alllinks:
        if os.path.exists(xss_conf):
            xss_conf = json.load(xss_conf)
            # payloads,blacklist will changed ++++++++++++++++++++++++++++++
        
        xss = xss(payloads, blacklist ,alllinks)
        xssLinks = xss.findxss()
        print 'xssLinks:'
        print xssLinks
elif results.target:
    ##singelscan()
    format_url = check_url(results.target)
    vulnerables = singlescan(format_url)

    if not vulnerables:
        exit(0)
    
    
    print ('vulnerables: '+vulnerables)
    exit(0)
else:
    parser.print_help()
    os._exit(0)

def check_url(url):
    if not url.startswith('http'):
        url = 'http://'+str(url)
    try:
        r = requests.get(url.split('?')[0], headers = headers)
        #r.status_code
        my.log(INFO,'status_code:'+str(r.status_code))
    except:
        my.log(INFO,'url请求异常!')
    return url