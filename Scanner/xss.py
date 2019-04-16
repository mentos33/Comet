import selenium

'''
接受Spider模块解析出的所有url，返回插入每个的结果
'''

payloads = ['<svg "ons>', '" onfocus="alert(1);', 'javascript:alert(1)', '"><svg/onload=alert`1`>']

blacklist = ['.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.avi', '.gif', '.svg',
             '.pdf']
xssLinks = [] 

class FindXss():
    