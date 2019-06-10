# -*- coding: utf-8 -*-
import pickle
import time
import requests
import random
import traceback 

class Spider:
    def __init__(self,domain='gsxt.gov.cn'):
        self.headers_51job={
            'Host': 'www.gsxt.gov.cn',
            #'Origin':'http://ehire.51job.com',
            'User-Agent':"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36""",
            'Accept': """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8""",
            'Accept-Language': """zh-CN,zh;q=0.9""",
            'Referer': """http://www.gsxt.gov.cn/index.html""",
            'Upgrade-Insecure-Requests':'1',
            'Connection': 'keep-alive'
        }
        self.s=requests.Session()
        self.s.headers=self.headers_51job
        self.__domain = domain
        self.timeOut = 30
        self.cookies = {}


    def SetLoginDomain(self,domain='gsxt.gov.cn'):
        """设置登录域名"""
        self.__domain=domain
        return self.__domain

    def SetTimeOut(self,timeOut=30):
        self.__timeOut=timeOut
        return self.__timeOut

    def set_cookies(self):
        """读取cookie文件 该文件由另外一个登录程序获取"""
        with open('D:/new.txt') as f:
            cookies = pickle.loads(f.read())
        for cookie in cookies:
            self.cookies[cookie['name']]=cookie['value']
        self.s.cookies.update(self.cookies)

    def open_url(self, url,data=None):
        """页面请求方法"""
        # 请求页面方法
        MaxTryTimes = 20
        waite_time = random.uniform(0, 1)  # 初始化等待时间
        for i in range(MaxTryTimes):
            time.sleep(waite_time)
            try:
                req = self.s.post(url,data=data,headers=self.headers_51job,timeout=self.timeOut)
                content=req.text
                if req.cookies.get_dict():
                    self.s.cookies.update(req.cookies)
                break
            except:
                traceback.print_exc()
                content = ''
        return content

if __name__ == '__main__':
    spider=Spider()
    spider.set_cookies()
    # content=spider.open_url(url='http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000')
    # print content