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

class my:
    BLUE = '\033[94m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def log(lvl, col, msg):
        logger.log(lvl, col + msg + my.END)


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
parser.add_argument("-t", dest="target", help="scan the specified website", metavar="example.com?x=1")

results = parser.parse_args()

Explain='''

Comet: A Simple Web Scanner Tool
Author: mentos
Email: mentos33@163.com
Usage: python comet.py --help

Comet is a simple tool for finding XSS and SQLI(SQL injection) in websites.
You can check XSS by '-u'.Check SQLI by '-t'.

'''
my.log(logging.INFO, my.BOLD+my.GREEN, Explain)

def check_url(url):
    if not url.startswith('http'):
        url = 'http://'+str(url)
    try:
        r = requests.get(url.split('?')[0], headers = headers)
        #r.status_code
        my.log(logging.INFO, my.GREEN, 'status_code:'+str(r.status_code))
    except:
        my.log(logging.WARNING, my.RED, 'url请求异常!')
    return url

def singlescan(url):
    "scan single targeted domain"

    if urlparse(url).query != '':
        result = sql.scan(url)
        if result != []:
            return result
        else:
            my.log(logging.INFO, my.GREEN, "no SQL injection vulnerability found")
    else:
        my.log(logging.ERROR, my.RED, 'parameters is required')
    return False
if results.url and results.target:
    parser.print_help()
    os._exit(0)
elif results.url:
    if not results.url:
        my.log(logging.WARNING, my.RED, 'url not null!')
        os._exit(-1)
    format_url = check_url(results.url)
    my.log(logging.INFO, my.GREEN, 'scanning {0}'.format(format_url))
    if results.cookies:
        my.log(logging.INFO, my.BLUE, 'use cookies : {0}'.format(results.cookies))
    mylink = link(format_url)
    count = 0
    alllinks = []
    if results.compOn:
        my.log(logging.INFO, my.GREEN, 'Doing a comprehensive traversal')
        alllinks = mylink.get_all_links()
    else:
        alllinks = mylink.get_links()
    with open('url_list.txt','w') as f:
        for _ in alllinks:
            f.write(_+"\n")
    my.log(logging.INFO, my.YELLOW, 'num of links : {0}'.format(str(len(alllinks))))
    #print 'num of links : '+str(len(alllinks))
    if alllinks:
        if os.path.exists(xss_conf):
            xss_conf = json.load(xss_conf)
            # payloads,blacklist will changed ++++++++++++++++++++++++++++++
        
        xss = xss(payloads, blacklist ,alllinks)
        xssLinks = xss.findxss()
        if xssLinks:
            my.log(logging.INFO, my.BOLD + my.GREEN, 'xss found!')
            for _ in xssLinks:
                my.log(logging.INFO, my.BOLD + my.GREEN, _)
        else:
            my.log(logging.INFO, my.YELLOW, 'xss not found!')
elif results.target:
    ##singelscan()
    format_url = check_url(results.target)
    my.log(logging.INFO, my.GREEN, 'scanning {0}'.format(format_url))
    vulnerables = singlescan(format_url)

    if not vulnerables:
        os._exit(0)
    my.log(logging.INFO, my.YELLOW, format_url+'is vulnerable')
    for _ in vulnerables:
        my.log(logging.INFO, my.BLUE, 'vulnerables: '+str(_))
    os._exit(0)
else:
    parser.print_help()
    os._exit(0)

