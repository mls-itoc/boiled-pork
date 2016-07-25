#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 気象庁データ(黄砂)をスクレイピングするプログラム
#
from pyquery import PyQuery as pq
from collections import OrderedDict
import pandas as pd
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

def main():
    # 取得したい地点名
    points = ["松江"]
    # 取得したい年のレンジ
    year_start = 2010
    year_end = 2016

    ipshell = InteractiveShellEmbed()

    for point in points:
      # 日付 数量 観測地点名
      header = ["date", "numberOfPoint", "isYellowDust"]

      column_count = len(header)
      data = OrderedDict()

      for i in range(0, column_count):
        data[ header[i] ] = []

      for year in range(year_start, year_end + 1):
        url = ("http://www.data.jma.go.jp/gmd/env/kosahp/kosa_table_{0}.html".format(year))
        query = pq(url, parser='html')
        day = query('.data tr')

        isSameLine = False;
        rowspan = 0

        for tr in day:
          if(len(data['date']) != len(data['isYellowDust'])):
            if(isSameLine):
              if(rowspan == 2):
                data['isYellowDust'].append(0);
            else:
              data['isYellowDust'].append(0);

          if isSameLine:
            for i, td in enumerate(tr):
              if pq(td).text() == point:
                key = header[2]
                data[key].append(1);

            rowspan -= 1
            if rowspan == 1:
              rowspan = 0
              isSameLine = False
          else:
            for i, td in enumerate(tr):
              if td.tag == "th":
                continue
              else:
                if td.attrib.has_key('rowspan'):
                  rowspan = int(td.attrib["rowspan"])
                  if rowspan > 1:
                    isSameLine = True

                if i >= 2: # 2 観測地点名
                  if pq(td).text() == point:
                    key = header[2]
                    data[key].append(1);

                else: # 0 日付 1 数量
                  key = header[i]
                  data[key].append(pq(td).text());

      if(len(data['date']) != len(data['isYellowDust'])):
        data['isYellowDust'].append(0);

      df = pd.DataFrame(data)
      df = pd.concat([df["date"], df["isYellowDust"]], axis=1)
      df.to_csv("yellow_dust.csv", index=False)

if __name__ == '__main__':
    main()
