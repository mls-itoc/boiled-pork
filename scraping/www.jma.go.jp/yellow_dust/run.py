#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 気象庁データのデータをスクレイピングするプログラム
#
from pyquery import PyQuery as pq
from collections import OrderedDict
import pandas as pd
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
import inspect

def each_slice(lis, n):
    s = 0
    while s < len(lis):
        yield lis[s:s+n]
        s += n

def main():
    header = ["date", "numberOfPoint", "isYellowDust"]

    # 日付 数量 観測地点名
    point = "松江"

    column_count = len(header)

    data = OrderedDict()

    for i in range(0, column_count):
      data[ header[i] ] = []

    year_start = 2005
    year_end = 2016

    ipshell = InteractiveShellEmbed()

    for year in range(year_start, year_end + 1):
      url = ("http://www.data.jma.go.jp/gmd/env/kosahp/kosa_table_{0}.html".format(year))
      query = pq(url, parser='html')
      day = query('.data tr')

      isSameLine = False;
      isFillBool = False;
      rowspan = 0
      #ipshell()

      for items in day: # itemsはtrのリスト
        #ipshell()
        if(len(data['date']) == len(data['isYellowDust'])):
          ""###
        else:
          #if((len(data['date']) > len(data['isYellowDust']))):
          if(isSameLine):
            if(rowspan == 2):
              data['isYellowDust'].append(0);
              isFillBool = True;
          else:
            data['isYellowDust'].append(0);

        if isSameLine:
          for i, item in enumerate(items): # item = td
            if pq(item).text() == point:
              key = header[2]
              data[key].append(1);
              isFillBool = True;

          rowspan -= 1
          if rowspan == 1:
            rowspan = 0
            isSameLine = False
        else:
          for i, item in enumerate(items): # item = td
            if item.tag == "th":
              continue
            else:
              # item = td
              if item.attrib.has_key('rowspan'):
                #ipshell()
                rowspan = int(item.attrib["rowspan"])
                if rowspan > 1:
                  isSameLine = True

              if i >= 2: # 2 観測地点名
                # tr
                if pq(item).text() == point:
                  #ipshell()
                  key = header[2]
                  data[key].append(1);
                  isFillBool = True;

              else: # 0 日付 1 数量
                dom = pq(item)
                key = header[i]
                data[key].append(pq(item).text());

    if(len(data['date']) == len(data['isYellowDust'])):
      ""###
    else:
      data['isYellowDust'].append(0);

    #ipshell()
    df = pd.DataFrame(data)
    df = pd.concat([df["date"], df["isYellowDust"]], axis=1)
    df.to_csv("yellow_sand.csv")

if __name__ == '__main__':
    main()
