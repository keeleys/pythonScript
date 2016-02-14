#!/usr/bin/python
# coding:utf-8

import urllib2
import urllib
import cookielib
import re
import sys
from bs4 import BeautifulSoup


class TbSpider:
    def __init__(self):
        # 设置cookie模式
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)

        self.loginUrl = "https://login.taobao.com"

    def login_tb(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        res = urllib2.Request(self.loginUrl, headers=headers)
        taobao = urllib2.urlopen(res)
        print taobao.read()


if __name__ == "__main__":
    try:
        TbSpider().login_tb()
    except urllib2.URLError, e:
        print e.reason
