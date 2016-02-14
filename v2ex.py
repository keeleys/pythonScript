# coding=utf-8

import urllib2
import urllib
import cookielib
import re
import sys
from bs4 import BeautifulSoup

headers = {
    'Host': 'www.v2ex.com',
    'Origin': 'http://www.v2ex.com',
    'referer': 'http://v2ex.com/signin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}


def main():
    if len(sys.argv) != 3:
        print "缺少参数,请跟用户名和密码"

    username = sys.argv[1]
    password = sys.argv[2]

    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)

    flag = login(username, password)
    if not flag:
        print "登陆失败,请检查用户名密码"
        sys.exit(-1)

    print "恭喜您登陆成功"

    daily()



def detail():
    url = "https://www.v2ex.com/balance";
    headers["referer"] = "https://www.v2ex.com/"
    res = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(res).read()

    soup = BeautifulSoup(content,"html.parser")
    balance = soup.find("a", class_="balance_area")
    moneys = list(balance.strings)
    print moneys


def index_form():
    try:
        resp = urllib2.urlopen("https://www.v2ex.com/signin");
    except urllib2.HTTPError, e:
        print "服务器出错了 %s" % e.code
        sys.exit(-1)

    resp_html = resp.read();
    pattern = re.compile(r'<input.*value="(\d+)".*name="once".*?')
    match = pattern.search(resp_html)
    return match.group(1)


def login(username, password):
    once = index_form()
    loginUrl = "https://www.v2ex.com/signin"
    param = {
        'u': username,
        'p': password,
        'once': once,
        'next': '/'
    }

    data = urllib.urlencode(param)
    loginReq = urllib2.Request(loginUrl, data, headers=headers)
    reqs = urllib2.urlopen(loginReq)
    content = reqs.read()
    m = re.search('登出', content)
    if m:
        return True
    else:
        return False


def get_once_url():
    url = "https://www.v2ex.com/mission/daily"
    data = urllib2.urlopen(url).read()
    p = '/mission/daily/redeem\?once=(\d+)'
    m = re.search(p, data)
    if m:
        return m.group(1)
    else:
        return None


def daily():
    once = get_once_url()
    if None == once:
        print '找不到once,您可能已经签到了'
        return
    url = "https://www.v2ex.com/mission/daily/redeem?once=%s" % once
    headers["referer"] = "https://www.v2ex.com/mission/daily"
    loginReq = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(loginReq);
    print "签到完毕"


if __name__ == "__main__":
    main();
