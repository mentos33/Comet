#!/usr/bin/env python
#coding=utf-8
import argparse
import logging
from urlparse import urlparse
import os
import json
from Spider.dynamic import link
from Scanner.xss import xss

'''
comet 的入口

'''


payloads = ['<svg "ons>', '" onfocus="alert(1);', 'javascript:alert(1)', '"><svg/onload=alert`1`>']

blacklist = ['.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.avi', '.gif', '.svg',
             '.pdf']


xss_conf = 'xss_conf.json'

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

#交互 接受参数  ''https:// 
parser = argparse.ArgumentParser()
parser.add_argument('-u', dest='url', help='URL of Target Website')
parser.add_argument('-c', dest='cookies', help='add cookies')
parser.add_argument('-e', action='store_true', dest='compOn',help='Enable comprehensive scan')

parser.add_argument("-t", dest="target", help="scan target website", metavar="www.example.com")

##################################
#save input args
results = parser.parse_args()
if results.url:
    pass
else:
    parser.print_help()
    os._exit(0)
# -t  pass


###############################
##link类
##########################

mylink = link(results.url)
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