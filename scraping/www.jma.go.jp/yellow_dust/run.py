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

    # 取得したい年のレンジ
    year_start = 2010
    year_end = 2016
    # 取得したい地点名
    # points = ["松江"]
    points = [
      ["札幌", 22, "北海道"],
      ["仙台", 41, "宮城県"],
      ["青森", 38, "青森県"],
      ["秋田", 37, "秋田県"],
      ["盛岡", 40, "岩手県"],
      ["山形", 43, "山形県"],
      ["福島", 39, "福島県"],
      ["東京", 35, "東京都"],
      ["宇都宮", 34, "栃木県"],
      ["前橋", 47, "群馬県"],
      ["熊谷", 33, "埼玉県"],
      ["水戸", 31, "茨城県"],
      ["銚子", 30, "千葉県"],
      ["横浜", 32, "神奈川県"],
      ["長野", 19, "長野県"],
      ["甲府", 36, "山梨県"],
      ["新潟", 42, "新潟県"],
      ["富山", 21, "富山県"],
      ["金沢", 17, "石川県"],
      ["福井", 23, "福井県"],
      ["静岡", 20, "静岡県"],
      ["岐阜", 16, "岐阜県"],
      ["津", 18, "三重県"],
      ["名古屋", 15, "愛知県"],
      ["大阪", 27, "大阪府"],
      ["京都", 25, "京都府"],
      ["奈良", 26, "奈良県"],
      ["彦根", 28, "滋賀県"],
      ["和歌山", 29, "和歌山県"],
      ["神戸", 24, "兵庫県"],
      ["鳥取", 4, "鳥取県"],
      ["松江", 3, "島根県"],
      ["岡山", 2, "岡山県"],
      ["広島", 1, "広島県"],
      ["高松", 11, "香川県"],
      ["松山", 10, "愛媛県"],
      ["徳島", 14, "徳島県"],
      ["高知", 12, "高知県"],
      ["福岡", 7, "福岡県"],
      ["下関", 5, "山口県"],
      ["大分", 13, "大分県"],
      ["佐賀", 6, "佐賀県"],
      ["熊本", 8, "熊本県"],
      ["長崎", 44, "長崎県"],
      ["宮崎", 9, "宮崎県"],
      ["鹿児島", 45, "鹿児島県"],
      ["那覇", 46, "沖縄県"]
    ]

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
        # if(len(data['isYellowDust']) != len(data['date']) ):
        #   ipshell()

        for tr in day:
          if(len(data['date']) != len(data['isYellowDust'])):
            if(isSameLine):
              print("same line")
              #if(rowspan == 2):
                #data['isYellowDust'].append(0);
            else:
              data['isYellowDust'].append(0);

          if isSameLine:
            for i, td in enumerate(tr):
              if pq(td).text() == point[0]:
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
                  if pq(td).text() == point[0]:
                    key = header[2]
                    data[key].append(1);

                else: # 0 日付 1 数量
                  key = header[i]
                  data[key].append(pq(td).text());

      if(len(data['date']) != len(data['isYellowDust'])):
        data['isYellowDust'].append(0);

      df = pd.DataFrame(data)
      df = pd.concat([df["date"], df["isYellowDust"]], axis=1)
      df.to_csv(str(point[1]) + ".csv", index=False)

if __name__ == '__main__':
    main()
