#!/usr/bin/env python3
#coding=utf-8
import argparse
import logging
from urllib.parse import urlparse
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

#交互 接受参数   -u "http://xxx.xx"   必须双引号或不加引号   还需要add补充 用户输入的 [http://] 等头信息
parser = argparse.ArgumentParser()
parser.add_argument('-u', dest='url', required=True ,help='URL of Target Website')
parser.add_argument('-c', dest='cookies', help='add cookies')

#save input args
results = parser.parse_args()
if not results.url:
    #logging()
    #print ('you could use [help] or [-h]')  不能输出？？
    print (results.url)

mylink = link(results.url)
count = 0
for url in mylink.get_links():
    
    assert isinstance(url, str),'link类返回的url不是字符串类型！！！'
    print (url)
    count +=1
print (count)
