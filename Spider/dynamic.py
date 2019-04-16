#!/usr/bin/env python3
#coding=utf-8
from selenium import webdriver
import requests
import time

#selenium 帮助找到站内连接
#find_by_tag(a)    只找了a标签的所有链接
class link():
    def __init__(self, url):
        
        options = webdriver.ChromeOptions()
        
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--test-type')
        

        self.driver = webdriver.Chrome(chrome_options = options)
        
        self.url = url
    def get_links(self):
        self.driver.get(self.url)
        time.sleep(3)
        urllist=[]
        for element in self.driver.find_elements_by_xpath('.//a'):
            urllist.append(element.get_attribute('href'))
        return urllist
    def __del__(self):
        self.driver.close()