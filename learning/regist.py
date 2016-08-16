import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import os
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
from sklearn.externals import joblib
import sqlite3
import time
from pyquery import PyQuery as pq
from collections import OrderedDict
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
ipshell = InteractiveShellEmbed()
from sklearn import preprocessing

def each_slice(lis, n):
    s = 0
    while s < len(lis):
        yield lis[s:s+n]
        s += n

def parse(three, four, five):
    ipshell = InteractiveShellEmbed()
    three["date"] = pd.to_datetime(three["date"])

    three.rename(columns={'temp': '3temp', 'dewPointTemp': '3dewPointTemp',
       'humid': '3humid', 'ap': '3ap', 'visibility': '3visibility',
       'windDirection': '3windDirection', 'windSpeed': '3windSpeed',
       'gustSpeed': '3gustSpeed', 'Precip': '3Precip', 'event': '3event',
       'situation': '3situation'}, inplace=True)

    four["date"] = pd.to_datetime(four["date"])

    four.rename(columns={'temp': '4temp', 'dewPointTemp': '4dewPointTemp',
       'humid': '4humid', 'ap': '4ap', 'visibility': '4visibility',
       'windDirection': '4windDirection', 'windSpeed': '4windSpeed',
       'gustSpeed': '4gustSpeed', 'Precip': '4Precip', 'event': '4event',
       'situation': '4situation'}, inplace=True)

    five["date"] = pd.to_datetime(five["date"])

    five.rename(columns={'temp': '5temp', 'dewPointTemp': '5dewPointTemp',
       'humid': '5humid', 'ap': '5ap', 'visibility': '5visibility',
       'windDirection': '5windDirection', 'windSpeed': '5windSpeed',
       'gustSpeed': '5gustSpeed', 'Precip': '5Precip', 'event': '5event',
       'situation': '5situation'}, inplace=True)

    df = pd.concat([three, four, five], axis=1)

    # 湿度
    df = df[ df["3humid"].isnull() == False ]
    df["3humid"] = df["3humid"].str.extract('([0-9]+)').astype(np.float)
    df['3humid2'] = df['3humid']
    df['3humid'] = df['3humid2'].astype(float)
    df.loc[df['3humid'].isnull(), '3humid']  = df["3humid"].mean()

    df = df[ df["4humid"].isnull() == False ]
    df["4humid"] = df["4humid"].str.extract('([0-9]+)').astype(np.float)
    df['4humid2'] = df['4humid']
    df['4humid'] = df['4humid2'].astype(float)
    df.loc[df['4humid'].isnull(), '4humid']  = df["4humid"].mean()

    df = df[ df["5humid"].isnull() == False ]
    df["5humid"] = df["5humid"].str.extract('([0-9]+)').astype(np.float)
    df['5humid2'] = df['5humid']
    df['5humid'] = df['5humid2'].astype(float)
    df.loc[df['5humid'].isnull(), '5humid']  = df["5humid"].mean()

    # 温度

    df = df[ df["3temp"].isnull() == False ]
    df["3temp"] = df["3temp"].str.extract('([0-9]+)').astype(np.float)
    df['3temp2'] = df['3temp']
    df['3temp'] = df['3temp2'].astype(float)
    df.loc[df['3temp'].isnull(), '3temp']  = df["3temp"].mean()

    df = df[ df["4temp"].isnull() == False ]
    df["4temp"] = df["4temp"].str.extract('([0-9]+)').astype(np.float)
    df['4temp2'] = df['4temp']
    df['4temp'] = df['4temp2'].astype(float)
    df.loc[df['4temp'].isnull(), '4temp']  = df["4temp"].mean()

    df = df[ df["5temp"].isnull() == False ]
    df["5temp"] = df["5temp"].str.extract('([0-9]+)').astype(np.float)
    df['5temp2'] = df['5temp']
    df['5temp'] = df['5temp2'].astype(float)
    df.loc[df['5temp'].isnull(), '5temp']  = df["4temp"].mean()

    df = df[ df["3dewPointTemp"].isnull() == False ]
    df["3dewPointTemp"] = df["3dewPointTemp"].str.extract('([0-9-]+)')
    df['3dewPointTemp2'] = df['3dewPointTemp']
    df.loc[df['3dewPointTemp'] == '-', '3dewPointTemp2'] = np.nan
    df['3dewPointTemp'] = df['3dewPointTemp2'].astype(float)
    df.loc[df['3dewPointTemp'].isnull(), '3dewPointTemp']  = df["3dewPointTemp"].mean()

    df = df[ df["4dewPointTemp"].isnull() == False ]
    df["4dewPointTemp"] = df["4dewPointTemp"].str.extract('([0-9-]+)')
    df['4dewPointTemp2'] = df['4dewPointTemp']
    df.loc[df['4dewPointTemp'] == '-', '4dewPointTemp2'] = np.nan
    df['4dewPointTemp'] = df['4dewPointTemp2'].astype(float)
    df.loc[df['4dewPointTemp'].isnull(), '4dewPointTemp']  = df["4dewPointTemp"].mean()

    df = df[ df["5dewPointTemp"].isnull() == False ]
    df["5dewPointTemp"] = df["5dewPointTemp"].str.extract('([0-9-]+)')
    df['5dewPointTemp2'] = df['5dewPointTemp']
    df.loc[df['5dewPointTemp'] == '-', '5dewPointTemp2'] = np.nan
    df['5dewPointTemp'] = df['5dewPointTemp2'].astype(float)
    df.loc[df['5dewPointTemp'].isnull(), '5dewPointTemp']  = df["5dewPointTemp"].mean()

    df["3ap"] = df["3ap"].str.extract('([0-9-]+)')
    df['3ap2'] = df['3ap']
    df.loc[df['3ap'] == '-', '3ap2'] = np.nan
    df['3ap'] = df['3ap2'].astype(float)
    df.loc[df['3ap'].isnull(), '3ap']  = df["3ap"].mean()

    df["4ap"] = df["4ap"].str.extract('([0-9-]+)')
    df['4ap2'] = df['4ap']
    df.loc[df['4ap'] == '-', '4ap2'] = np.nan
    df['4ap'] = df['4ap2'].astype(float)
    df.loc[df['4ap'].isnull(), '4ap']  = df["4ap"].mean()

    df["5ap"] = df["5ap"].str.extract('([0-9-]+)')
    df['5ap2'] = df['5ap']
    df.loc[df['5ap'] == '-', '5ap2'] = np.nan
    df['5ap'] = df['5ap2'].astype(float)
    df.loc[df['5ap'].isnull(), '5ap']  = df["5ap"].mean()


    df["3visibility"] = df["3visibility"].str.extract('([0-9-]+)')
    df['3visibility2'] = df['3visibility']
    df.loc[df['3visibility'] == '-', '3visibility2'] = np.nan
    df['3visibility'] = df['3visibility2'].astype(float)
    df.loc[df['3visibility'].isnull(), '3visibility']  = df["3visibility"].mean()

    df["4visibility"] = df["4visibility"].str.extract('([0-9-]+)')
    df['4visibility2'] = df['4visibility']
    df.loc[df['4visibility'] == '-', '4visibility2'] = np.nan
    df['4visibility'] = df['4visibility2'].astype(float)
    df.loc[df['4visibility'].isnull(), '4visibility']  = df["4visibility"].mean()

    df["5visibility"] = df["5visibility"].str.extract('([0-9-]+)')
    df['5visibility2'] = df['5visibility']
    df.loc[df['5visibility'] == '-', '5visibility2'] = np.nan
    df['5visibility'] = df['5visibility2'].astype(float)
    df.loc[df['5visibility'].isnull(), '5visibility']  = df["5visibility"].mean()

    df["3windSpeed"] = df["3windSpeed"].str.extract('([0-9.]+)')
    df['3windSpeed2'] = df['3windSpeed']
    df['3windSpeed'] = df['3windSpeed2'].astype(float)
    df.loc[df['3windSpeed'].isnull(), '3windSpeed']  = df["3windSpeed"].mean()

    df["4windSpeed"] = df["4windSpeed"].str.extract('([0-9.]+)')
    df['4windSpeed2'] = df['4windSpeed']
    df['4windSpeed'] = df['4windSpeed2'].astype(float)
    df.loc[df['4windSpeed'].isnull(), '4windSpeed']  = df["4windSpeed"].mean()

    df["5windSpeed"] = df["5windSpeed"].str.extract('([0-9.]+)')
    df['5windSpeed2'] = df['5windSpeed']
    df['5windSpeed'] = df['5windSpeed2'].astype(float)
    df.loc[df['5windSpeed'].isnull(), '5windSpeed']  = df["5windSpeed"].mean()

    df_direction_3 = pd.get_dummies(df["3windDirection"], prefix="3")
    df_direction_4 = pd.get_dummies(df["4windDirection"], prefix="4")
    df_direction_5 = pd.get_dummies(df["5windDirection"], prefix="5")

    not_needed = ["date", "time"
      "3time", "3ap","3gustSpeed", "3Precip", "3event", "3situation", "3humid2", "3temp2", "3dewPointTemp2", "3ap2", "3visibility2", "3windSpeed2",
      "4time", "4ap","4gustSpeed", "4Precip", "4event", "4situation", "4humid2", "4temp2", "4dewPointTemp2", "4ap2", "4visibility2", "4windSpeed2",
      "5time", "5ap","5gustSpeed", "5Precip", "5event", "5situation", "5humid2", "5temp2", "5dewPointTemp2", "5ap2", "5visibility2", "5windSpeed2"
    ]

    df = pd.concat([
     df["3dewPointTemp"], df["3windSpeed"], df["3humid"],  df["3temp"], df_direction_3, df["3visibility"],
     df["4dewPointTemp"], df["4windSpeed"], df["4humid"],  df["4temp"], df_direction_4, df["4visibility"],
     df["5dewPointTemp"], df["5windSpeed"], df["5humid"],  df["5temp"], df_direction_5, df["5visibility"]], axis=1)

    d_columns = ["3_Calm", "3_ENE", "3_ESE",	"3_East", "3_NE", "3_NNE", "3_NNW", "3_NW", "3_North", "3_SE", "3_SSE", "3_SSW", "3_SW", "3_South", "3_WNW", "3_WSW", "3_West",
     "4_Calm", "4_ENE", "4_ESE",	"4_East", "4_NE", "4_NNE", "4_NNW", "4_NW", "4_North", "4_SE", "4_SSE", "4_SSW", "4_SW", "4_South", "4_WNW", "4_WSW", "4_West",
     "5_Calm", "5_ENE", "5_ESE",	"5_East", "5_NE", "5_NNE", "5_NNW", "5_NW", "5_North", "5_SE", "5_SSE", "5_SSW", "5_SW", "5_South", "5_WNW", "5_WSW", "5_West"]

    for col in d_columns:
        if col in df.index:
            print("exist!")
        else:
          df[col] = 0.0

    X = df.as_matrix()
    X = preprocessing.scale(X)
    return X

def scraip(year, month, day):
    header =  [ "time", "temp", "dewPointTemp", "humid", "ap", "visibility", "windDirection", "windSpeed", "gustSpeed", "Precip", "event", "situation"]

    column_count = len(header)

    data = OrderedDict()
    data['date'] = []

    for i in range(0, column_count):
      data[ header[i] ] = []

    block_no = 57297 # 57297 Xinyang 52866  xing
    url = ('https://www.wunderground.com/history/wmo/{0}/{1}/{2}/{3}/DailyHistory.html?req_city=Omno-Gobi&req_statename=Mongolia&reqdb.zip=00000&reqdb.magic=1&reqdb.wmo={4}'.format(block_no, year, month, day, block_no))
    query = pq(url, parser='html')
    row = query('.obs-table tbody .no-metars td')

    for items in each_slice(row, column_count):
          for i, item in enumerate(items):
              key = header[i]
              data[key].append(pq(item).text());

    l = int(len(row) / column_count)

    for j in range(l):
        data['date'].append('%s/%s/%s' % (year, month, day))

    df = pd.DataFrame(data)
    return df


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

conn = sqlite3.connect('../backend/db/development.sqlite3')
cur = conn.cursor()
today = dt.now()
three_days_ago = today - timedelta(days=3)
four_days_ago = today - timedelta(days=4)
five_days_ago = today - timedelta(days=5)
today = today.strftime('%Y-%m-%d')

three_days_ago_data = scraip(three_days_ago.year, three_days_ago.month, three_days_ago.day)
four_days_ago_data = scraip(four_days_ago.year, four_days_ago.month, four_days_ago.day)
five_days_ago_data = scraip(five_days_ago.year, five_days_ago.month, five_days_ago.day)

for point in points:
  model = joblib.load("./models/" + str(point[1]) + "/model.pkl")
  X= parse(three_days_ago_data, four_days_ago_data, five_days_ago_data)
  yy = []
  for xx in X:
    yy.append(model.predict(xx.reshape(1,len(xx)))[0])

  average = sum(yy) / len(yy)

  if average > 0:
    cur.execute(" INSERT INTO predictions(date, yellow_dust, pref_id) VALUES(?, ?, ?)", (today, 1, point[1]))

conn.commit()
conn.close()
