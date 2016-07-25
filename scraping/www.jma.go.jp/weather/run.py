#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 気象庁データのデータをスクレイピングするプログラム
#
from pyquery import PyQuery as pq
from collections import OrderedDict
import pandas as pd
# from IPython import embed
# from IPython.terminal.embed import InteractiveShellEmbed

def each_slice(lis, n):
    s = 0
    while s < len(lis):
        yield lis[s:s+n]
        s += n

def main():
    header = ['気圧(hPa)現地平均', '気圧(hPa)海面平均',
              '降水量(mm)合計', '降水量(mm)最大1時間', '降水量(mm)最大10分間',
              '気温(℃)平均', '気温(℃)最高', '気温(℃)最低', '湿度(％)平均', '湿度(％)最小',
              '風向・風速(m/s)平均風速', '風向・風速(m/s)最大風速 風速', '風向・風速(m/s)最大風速 風向',
              '風向・風速(m/s)最大瞬間風速 風速', '風向・風速(m/s)最大瞬間風速 風向',
              '日照時間(h)', '雪(cm)降雪合計', '雪(cm)最深積雪値',
              '天気概況 昼(06:00-18:00)','天気概況 夜(18:00-翌日06:00)']

    column_count = len(header)

    data = OrderedDict()
    data['年月日'] = []

    for i in range(0, column_count):
      data[ header[i] ] = []

    # 松江を表すコード
    prec_no = 68
    block_no = 47741

    year_start = 2013
    year_end = 2016

    # ipshell = InteractiveShellEmbed()

    for year in range(year_start, year_end + 1):
      for month in range(1, 12):

        url = ('http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?'
               'prec_no={0}&block_no={1}&year={2}&month={3}&day=&view='.format(prec_no, block_no, year, month))
        query = pq(url, parser='html')
        day = query('.data_0_0')

        for items in each_slice(day, column_count):
          for i, item in enumerate(items):
            key = header[i]
            data[key].append(pq(item).text());

        l = int(len(day) / column_count)

        for j in range(l):
          data['年月日'].append('%s/%s/%s' % (year, month, j+1))

    #ipshell()

    df = pd.DataFrame(data)
    df.to_csv("weather.csv")

if __name__ == '__main__':
    main()
