#!/usr/bin/python
# coding:utf-8

import urllib2
import urllib
import cookielib
import re
import bs4

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

index_url = "http://www.baidu.com/"
token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login"
login_url = "https://passport.baidu.com/v2/api/?login"

username = '偷你一笑'
password = 'x230381871'

# 访问首页拿到cookie
urllib2.urlopen(index_url)
print cookie

# 获取token,
tokenReturn = urllib2.urlopen(token_url);
matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"', tokenReturn.read());
tokenVal = matchVal.group('tokenVal');

postData = {
    'username': username,
    'password': password,
    'u': 'https://passport.baidu.com/',
    'tpl': 'pp',
    'token': tokenVal,
    'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
    'isPhone': 'false',
    'charset': 'UTF-8',
    'callback': 'parent.bd__pcbs__ra48vi'
}
postData = urllib.urlencode(postData);

# 发送登录请求
loginRequest = urllib2.Request(login_url,postData);
loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch');
loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded');
sendPost = urllib2.urlopen(loginRequest);

teibaUrl = 'http://tieba.baidu.com/f/like/mylike?v=1387441831248'
content = urllib2.urlopen(teibaUrl).read();
content = content.decode('gbk').encode('utf8');

soup = bs4.BeautifulSoup(content, "html.parser");
list = soup.findAll('tr')
list = list[1:len(list)]

endpage = re.search(r'<a.*=(\d*)">尾页</a>',content)
print endpage.group()
for i in range(1, int(endpage.group(1))+1):
    print i
# print range(1,int(endpage.group(1)))
