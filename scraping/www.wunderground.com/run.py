#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# wundergroundデータのデータをスクレイピングするプログラム
#
import time
from pyquery import PyQuery as pq
from collections import OrderedDict
import pandas as pd
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
import random

def each_slice(lis, n):
    s = 0
    while s < len(lis):
        yield lis[s:s+n]
        s += n

def main():
    header =  [ "時間 (ULAT)", "温度", "露点温度", "湿度", "気圧", "視程", "Wind Dir", "風速", "突風の速度", "Precip", "イベント", "現在の気象状況"]

    column_count = len(header)

    data = OrderedDict()
    data['年月日'] = []

    for i in range(0, column_count):
      data[ header[i] ] = []

    block_no = 44215
    year_start = 2016
    year_end = 2016
    ipshell = InteractiveShellEmbed()

    for year in range(year_start, year_end + 1):
        for month in range(5, 12):
          for day in range(1, 31):
              random.randint(1, 3)
              url = ('https://www.wunderground.com/history/wmo/{0}/{1}/{2}/{3}/DailyHistory.html?req_city=Omno-Gobi&req_statename=Mongolia&reqdb.zip=00000&reqdb.magic=1&reqdb.wmo={4}'.format(block_no, year, month, day, block_no))
              query = pq(url, parser='html')
              row = query('.obs-table tbody .no-metars td')

              for items in each_slice(row, column_count):
                  for i, item in enumerate(items):
                      key = header[i]
                      data[key].append(pq(item).text());

              l = int(len(row) / column_count)

              for j in range(l):
                data['年月日'].append('%s年%s月%s日' % (year, month, day))

    df = pd.DataFrame(data)
    df.to_csv("weather.csv")

if __name__ == '__main__':
    main()
