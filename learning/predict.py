
# In[4]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import timedelta
import os
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed


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

y_path = "../../scraping/www.jma.go.jp/yellow_dust/"

for point in points:

  df_yellow = pd.read_csv(y_path + str(point[1]) + ".csv", header=0)
  # In[182]:

  df_yellow["date"] = pd.to_datetime(df_yellow["date"])


  # In[183]:

  df_gobi = pd.read_csv("./xinyang.csv", header=0)
  # ゴビ砂漠・黄土高原から日本に黄砂が到達するまで、概ね3〜4日程度かかる。
  #df_gobi_displaced_1day =  pd.read_csv("./omno-gobi.csv", header=0)

  df_gobi_displaced_3day =  pd.read_csv("./xinyang3.csv", header=0)
  df_gobi_displaced_4day =  pd.read_csv("./xinyang4.csv", header=0)
  df_gobi_displaced_5day =  pd.read_csv("./xinyang5.csv", header=0)


  # In[184]:

  df_gobi["date"] = pd.to_datetime(df_gobi["date"]) #, df_gobi["time"])

  df_gobi_displaced_3day["date"] = pd.to_datetime(df_gobi_displaced_3day["date"])
  df_gobi_displaced_4day["date"] = pd.to_datetime(df_gobi_displaced_4day["date"])
  df_gobi_displaced_5day["date"] = pd.to_datetime(df_gobi_displaced_5day["date"])


  # In[185]:


  df_gobi_displaced_3day["date"] = df_gobi_displaced_3day["date"] + timedelta(days=3)
  df_gobi_displaced_4day["date"] = df_gobi_displaced_4day["date"]  + timedelta(days=4)
  df_gobi_displaced_5day["date"] = df_gobi_displaced_5day["date"] + timedelta(days=5)


  # In[186]:

  df_3_4 = pd.merge(df_gobi_displaced_3day, df_gobi_displaced_4day, on=["date", "time"], how="inner")
  df_all = pd.merge(df_3_4, df_gobi_displaced_5day, on=["date", "time"], how="inner")


  # In[187]:

  df_all


  # In[188]:

  df_gobi = pd.merge(df_all, df_yellow, on="date" , how="outer" )
  df_gobi["isYellowDust"] = df_gobi["isYellowDust"].fillna(0)


  # In[189]:

  # 湿度

  df_gobi = df_gobi[ df_gobi["3humid"].isnull() == False ]
  df_gobi["3humid"] = df_gobi["3humid"].str.extract('([0-9]+)').astype(np.float)
  df_gobi['3humid2'] = df_gobi['3humid']
  df_gobi['3humid'] = df_gobi['3humid2'].astype(float)
  df_gobi.loc[df_gobi['3humid'].isnull(), '3humid']  = df_gobi["3humid"].mean()

  df_gobi = df_gobi[ df_gobi["4humid"].isnull() == False ]
  df_gobi["4humid"] = df_gobi["4humid"].str.extract('([0-9]+)').astype(np.float)
  df_gobi['4humid2'] = df_gobi['4humid']
  df_gobi['4humid'] = df_gobi['4humid2'].astype(float)
  df_gobi.loc[df_gobi['4humid'].isnull(), '4humid']  = df_gobi["4humid"].mean()

  df_gobi = df_gobi[ df_gobi["5humid"].isnull() == False ]
  df_gobi["5humid"] = df_gobi["5humid"].str.extract('([0-9]+)').astype(np.float)
  df_gobi['5humid2'] = df_gobi['5humid']
  df_gobi['5humid'] = df_gobi['5humid2'].astype(float)
  df_gobi.loc[df_gobi['5humid'].isnull(), '5humid']  = df_gobi["5humid"].mean()

  # 温度

  df_gobi = df_gobi[ df_gobi["3temp"].isnull() == False ]
  df_gobi["3temp"] = df_gobi["3temp"].str.extract('([0-9]+)').astype(np.float)
  df_gobi['3temp2'] = df_gobi['3temp']
  df_gobi['3temp'] = df_gobi['3temp2'].astype(float)
  df_gobi.loc[df_gobi['3temp'].isnull(), '3temp']  = df_gobi["3temp"].mean()

  df_gobi = df_gobi[ df_gobi["4temp"].isnull() == False ]
  df_gobi["4temp"] = df_gobi["4temp"].str.extract('([0-9]+)').astype(np.float)
  df_gobi['4temp2'] = df_gobi['4temp']
  df_gobi['4temp'] = df_gobi['4temp2'].astype(float)
  df_gobi.loc[df_gobi['4temp'].isnull(), '4temp']  = df_gobi["4temp"].mean()

  df_gobi = df_gobi[ df_gobi["5temp"].isnull() == False ]
  df_gobi["5temp"] = df_gobi["5temp"].str.extract('([0-9]+)').astype(np.float)
  df_gobi['5temp2'] = df_gobi['5temp']
  df_gobi['5temp'] = df_gobi['5temp2'].astype(float)
  df_gobi.loc[df_gobi['5temp'].isnull(), '5temp']  = df_gobi["4temp"].mean()


  #

  df_gobi = df_gobi[ df_gobi["3dewPointTemp"].isnull() == False ]
  df_gobi["3dewPointTemp"] = df_gobi["3dewPointTemp"].str.extract('([0-9-]+)')
  df_gobi['3dewPointTemp2'] = df_gobi['3dewPointTemp']
  df_gobi.loc[df_gobi['3dewPointTemp'] == '-', '3dewPointTemp2'] = np.nan
  df_gobi['3dewPointTemp'] = df_gobi['3dewPointTemp2'].astype(float)
  df_gobi.loc[df_gobi['3dewPointTemp'].isnull(), '3dewPointTemp']  = df_gobi["3dewPointTemp"].mean()

  df_gobi = df_gobi[ df_gobi["4dewPointTemp"].isnull() == False ]
  df_gobi["4dewPointTemp"] = df_gobi["4dewPointTemp"].str.extract('([0-9-]+)')
  df_gobi['4dewPointTemp2'] = df_gobi['4dewPointTemp']
  df_gobi.loc[df_gobi['4dewPointTemp'] == '-', '4dewPointTemp2'] = np.nan
  df_gobi['4dewPointTemp'] = df_gobi['4dewPointTemp2'].astype(float)
  df_gobi.loc[df_gobi['4dewPointTemp'].isnull(), '4dewPointTemp']  = df_gobi["4dewPointTemp"].mean()

  df_gobi = df_gobi[ df_gobi["5dewPointTemp"].isnull() == False ]
  df_gobi["5dewPointTemp"] = df_gobi["5dewPointTemp"].str.extract('([0-9-]+)')
  df_gobi['5dewPointTemp2'] = df_gobi['5dewPointTemp']
  df_gobi.loc[df_gobi['5dewPointTemp'] == '-', '5dewPointTemp2'] = np.nan
  df_gobi['5dewPointTemp'] = df_gobi['5dewPointTemp2'].astype(float)
  df_gobi.loc[df_gobi['5dewPointTemp'].isnull(), '5dewPointTemp']  = df_gobi["5dewPointTemp"].mean()

  #
  #df_gobi = df_gobi[ df_gobi["3ap"].isnull() == False ]


  df_gobi["3ap"] = df_gobi["3ap"].str.extract('([0-9-]+)')
  df_gobi['3ap2'] = df_gobi['3ap']
  df_gobi.loc[df_gobi['3ap'] == '-', '3ap2'] = np.nan
  df_gobi['3ap'] = df_gobi['3ap2'].astype(float)
  df_gobi.loc[df_gobi['3ap'].isnull(), '3ap']  = df_gobi["3ap"].mean()

  #df_gobi = df_gobi[ df_gobi["4ap"].isnull() == False ]

  df_gobi["4ap"] = df_gobi["4ap"].str.extract('([0-9-]+)')
  df_gobi['4ap2'] = df_gobi['4ap']
  df_gobi.loc[df_gobi['4ap'] == '-', '4ap2'] = np.nan
  df_gobi['4ap'] = df_gobi['4ap2'].astype(float)
  df_gobi.loc[df_gobi['4ap'].isnull(), '4ap']  = df_gobi["4ap"].mean()

  df_gobi["5ap"] = df_gobi["5ap"].str.extract('([0-9-]+)')
  df_gobi['5ap2'] = df_gobi['5ap']
  df_gobi.loc[df_gobi['5ap'] == '-', '5ap2'] = np.nan
  df_gobi['5ap'] = df_gobi['5ap2'].astype(float)
  df_gobi.loc[df_gobi['5ap'].isnull(), '5ap']  = df_gobi["5ap"].mean()


  #
  df_gobi["3visibility"] = df_gobi["3visibility"].str.extract('([0-9-]+)')
  df_gobi['3visibility2'] = df_gobi['3visibility']
  df_gobi.loc[df_gobi['3visibility'] == '-', '3visibility2'] = np.nan
  df_gobi['3visibility'] = df_gobi['3visibility2'].astype(float)
  df_gobi.loc[df_gobi['3visibility'].isnull(), '3visibility']  = df_gobi["3visibility"].mean()

  df_gobi["4visibility"] = df_gobi["4visibility"].str.extract('([0-9-]+)')
  df_gobi['4visibility2'] = df_gobi['4visibility']
  df_gobi.loc[df_gobi['4visibility'] == '-', '4visibility2'] = np.nan
  df_gobi['4visibility'] = df_gobi['4visibility2'].astype(float)
  df_gobi.loc[df_gobi['4visibility'].isnull(), '4visibility']  = df_gobi["4visibility"].mean()

  df_gobi["5visibility"] = df_gobi["5visibility"].str.extract('([0-9-]+)')
  df_gobi['5visibility2'] = df_gobi['5visibility']
  df_gobi.loc[df_gobi['5visibility'] == '-', '5visibility2'] = np.nan
  df_gobi['5visibility'] = df_gobi['5visibility2'].astype(float)
  df_gobi.loc[df_gobi['5visibility'].isnull(), '5visibility']  = df_gobi["5visibility"].mean()

  #

  df_gobi["3windSpeed"] = df_gobi["3windSpeed"].str.extract('([0-9.]+)')
  df_gobi['3windSpeed2'] = df_gobi['3windSpeed']
  df_gobi['3windSpeed'] = df_gobi['3windSpeed2'].astype(float)
  df_gobi.loc[df_gobi['3windSpeed'].isnull(), '3windSpeed']  = df_gobi["3windSpeed"].mean()

  df_gobi["4windSpeed"] = df_gobi["4windSpeed"].str.extract('([0-9.]+)')
  df_gobi['4windSpeed2'] = df_gobi['4windSpeed']
  df_gobi['4windSpeed'] = df_gobi['4windSpeed2'].astype(float)
  df_gobi.loc[df_gobi['4windSpeed'].isnull(), '4windSpeed']  = df_gobi["4windSpeed"].mean()

  df_gobi["5windSpeed"] = df_gobi["5windSpeed"].str.extract('([0-9.]+)')
  df_gobi['5windSpeed2'] = df_gobi['5windSpeed']
  df_gobi['5windSpeed'] = df_gobi['5windSpeed2'].astype(float)
  df_gobi.loc[df_gobi['5windSpeed'].isnull(), '5windSpeed']  = df_gobi["5windSpeed"].mean()


  # In[190]:

  df_gobi = df_gobi[ df_gobi["time"].isnull() == False ]


  # In[191]:


  df_direction_3 = pd.get_dummies(df_gobi["3windDirection"], prefix="3")
  df_direction_4 = pd.get_dummies(df_gobi["4windDirection"], prefix="4")
  df_direction_5 = pd.get_dummies(df_gobi["5windDirection"], prefix="5")


  # In[192]:


  # df_event_3 =  pd.get_dummies(df_gobi["3event"], prefix="3")
  # df_event_4 =  pd.get_dummies(df_gobi["4event"], prefix="4")
  # df_event_5 =  pd.get_dummies(df_gobi["5event"], prefix="5")


  # In[193]:

  not_needed = [
  "3time", "3ap","3gustSpeed", "3Precip", "3event", "3situation", "3humid2", "3temp2", "3dewPointTemp2", "3ap2", "3visibility2", "3windSpeed2",
  "4time", "4ap","4gustSpeed", "4Precip", "4event", "4situation", "4humid2", "4temp2", "4dewPointTemp2", "4ap2", "4visibility2", "4windSpeed2",
  "5time", "5ap","5gustSpeed", "5Precip", "5event", "5situation", "5humid2", "5temp2", "5dewPointTemp2", "5ap2", "5visibility2", "5windSpeed2"
  ]


  # In[194]:

  df = pd.concat([ df_gobi["isYellowDust"],
       df_gobi["3dewPointTemp"], df_gobi["3windSpeed"], df_gobi["3humid"],  df_gobi["3temp"], df_direction_3, df_gobi["3visibility"],
       df_gobi["4dewPointTemp"], df_gobi["4windSpeed"], df_gobi["4humid"],  df_gobi["4temp"], df_direction_4, df_gobi["4visibility"],
       df_gobi["5dewPointTemp"], df_gobi["5windSpeed"], df_gobi["5humid"],  df_gobi["5temp"], df_direction_5, df_gobi["5visibility"]], axis=1)
  #[df_gobi["date"],
  # [df_gobi["dewPointTemp"], df_gobi["windSpeed"], df_gobi["isYellowDust"], df_gobi["humid"],  df_gobi["temp"], df_direction, df_gobi["visibility"]


  # In[195]:

  df_y =  df["isYellowDust"]
  y = df_y.as_matrix()


  # In[196]:

  df_X = df.drop("isYellowDust", axis=1)


  # In[197]:


  # In[198]:

  df_X


  # In[132]:

  X = df_X.as_matrix()


  # In[133]:

  X = df_X.as_matrix()

  print(df_X.shape)
  # In[134]:

  X.std(axis=0)


  # In[135]:

  from sklearn import preprocessing


  # In[136]:

  X = preprocessing.scale(X)


  # In[137]:

  X.std(axis=0)

    # In[26]:

    # ラベル付きデータをトレーニングセットとテストセットに分割するためのモジュールを読み込む
  from sklearn import cross_validation


  # In[27]:

  # ラベル付きデータをトレーニングセット (X_train, y_train)とテストセット (X_test, y_test)に分割
  X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.2, random_state=42)


  # In[28]:

  # まずは簡単なモデルで試してみよう

  # === 線形モデル ===
  # モジュールの読み込み
  #from sklearn import linear_model
  #  モデル構築
  #model = linear_model.LogisticRegression()

  # === サポートベクターマシン ===
  # モジュールの読み込み
  #from sklearn import svm
  #  モデル構築
  #model = svm.SVC()

  # === K最近傍法 ===
  # モジュールの読み込み
  #from sklearn.neighbors import KNeighborsClassifier
  #  モデル構築
  #model = KNeighborsClassifier()

  # === ランダムフォレスト ===
  # モジュールの読み込み
  from sklearn import ensemble
  #  モデル構築
  model = ensemble.RandomForestClassifier(n_estimators=5, max_depth=10)

  # === 勾配ブースティング ===
  # モジュールの読み込み
  #from sklearn import ensemble
  #  モデル構築
  #model = ensemble.GradientBoostingClassifier()

  # print(X_train.shape)
  # print(y_train.shape)
  # ipshell = InteractiveShellEmbed()
  # ipshell()
  model.fit(X_train, y_train)

  # In[29]:

  from sklearn.externals import joblib

  if not os.path.exists("./models/" + str(point[1])):
    os.makedirs("./models/" + str(point[1]))

  # In[32]:
  joblib.dump(model, "./models/" + str(point[1]) + "/" + 'model.pkl')
  print("Done: ", str(point[2]))
