#!/usr/bin/env python
#coding=utf-8
import mechanize
import requests

#mechanize 帮助找到站内连接
class link():
    
    
    
    def __init__(self, url):
        br = mechanize.Browser()
        br.addheaders = [
            ('User-agent',
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')
        ]
        br.set_handle_robots(False)
        br.set_handle_refresh(False)

        self.br = br
        self.url = url
    def get_links(self):
        domains = []
        self.br.open(self.url)
        for link in self.br.links():
            if self.url in str(link.absolute_url):
                domains.append(str(link.absolute_url))
        domains = list(set(domains))    
        #logging(the num of links are : len(domains))
        return domains
    def get_all_links(self):
        largeNumberOfUrls = []
        domains = self.get_links()
        for link in domains:
            self.br.open(link)
            self.br._factory.is_html = True
            # going deeper into each link and finding its links
            for newlink in self.br.links():
                if self.url in str(newlink.absolute_url):
                    largeNumberOfUrls.append(newlink.absolute_url)
        domains = list(set(domains + largeNumberOfUrls))
        #logging
        return domains