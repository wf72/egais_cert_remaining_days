#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import sys
import re
import time


def get_cert_end_date(utm_url, sert_type):
    """get date from url"""
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


def date_to_epoch(d):
    """Convert date to epoch"""
    pattern = '%Y-%m-%d %H:%M:%S'
    return int(time.mktime(time.strptime(d, pattern)))


if __name__ == '__main__':
    '''Возвращает количество дней, до завершения дейтсвия сертификата
Первый параметр адрес хоста
Второй параметр тип сертификата: ГОСТ или PKI'''
    if sys.argv[1] and sys.argv[2]:
        sert_date = get_cert_end_date("http://%s:8080" % sys.argv[1], sys.argv[2])
        if sert_date:
            print(int((date_to_epoch(sert_date) - int(time.time()))/86400))
