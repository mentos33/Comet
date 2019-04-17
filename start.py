#!/usr/bin/env python
#coding=utf-8
import argparse
import logging
import urlparse
from Spider.dynamic import link


'''
comet 的入口

'''

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
parser.add_argument('-u', dest='url', required=True ,help='URL of Target Website')
parser.add_argument('-c', dest='cookies', help='add cookies')
parser.add_argument('-e', action='store_true', dest='compOn',help='Enable comprehensive scan')

#save input args
results = parser.parse_args()
if not results.url:
    #logging()
    #print ('you could use [help] or [-h]')  不能输出？？
    results.url

###############################
##link类
##########################

mylink = link(results.url)
count = 0
alllinks = []
if results.conpOn:
    alllinks = mylink.get_all_links()
else:
    alllinks = mylink.get_links()
for url in alllinks:
    
    #assert isinstance(url, str),'link类返回的url不是字符串类型！！！'
    print (url)
    count +=1
print (count)