import mechnize
import requests

#mechnize 帮助找到站内连接
class link():
    def __init__(self, url):
        br = mechnize.Browser()
        br.addheaders = [
            ('User-agent',
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')
        ]
        br.set_handle_robots(False)
        br.set_handle_refresh(False)

        self.br = br
        self.url = url
    def get_links(self):
        self.br.open(self.url)
        for link in br.links():
            if smallurl in str(link.absolute_url):
                domains.append(str(link.absolute_url))
        domains = list(set(domains))    
        #logging(the num of links are : len(domains))
        return domains
    def get_all_links(self):
        for link in self.get_links():
            br.open(link)
                # going deeper into each link and finding its links
                for newlink in br.links():
                    if smallurl in str(newlink.absolute_url):
                        largeNumberOfUrls.append(newlink.absolute_url)
        domains = list(set(domains + largeNumberOfUrls))
        #logging
        return domains