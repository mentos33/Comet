#!/usr/bin/env python3
#coding=utf-8
import argparse
import logging
from urllib.parse import urlparse



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

#交互 接受参数
parser = argparse.ArgumentParser()
parser.add_argument('-u', dest='url', required=True ,help='URL of Target Website')
parser.add_argument('-c', dest='cookies', help='add cookies')

#save input args
results = parser.parse_args()
if results.url:
    pass
else:
    #logging()
    #print ('you could use [help] or [-h]')  不能输出？？
    print (results.url)
    

