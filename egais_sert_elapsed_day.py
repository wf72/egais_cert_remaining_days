#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import sys
import re
import time


def get_sert_exp_date(utm_url, sert_type):
    try:
        page = urllib.request.urlopen(utm_url)
    except urllib.error.URLError as e:
        print(e)
        return None
    soup = BeautifulSoup(page.read())
    for pre in soup.find_all('pre'):
        for s in pre.stripped_strings:
            pattern = "%s\:.+по ([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2})" % sert_type
            m = re.search(pattern, s)
            if m:
                return m.group(1)


def date_to_epoch(sert_date):
    pattern = '%Y-%m-%d %H:%M:%S'
    return int(time.mktime(time.strptime(sert_date, pattern)))


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2]:
        sert_date = get_sert_exp_date("http://%s:8080" % sys.argv[1], sys.argv[2])
        if sert_date:
            print(int((date_to_epoch(sert_date) - int(time.time()))/86400))
