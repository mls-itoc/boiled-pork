# 風邪データから黄砂への学習予測に使えそうなデータを作成する
# auther:Mitsuaki Ihara

## 風力 風速と被ってる
### power (MW)

## 気温
### air temperature at 2m (K)

## 方角 ☆
### wind direction at 100m (deg)

## 日時 ☆
### Year,Month,Day,Hour,Minute	

## 風速 ☆
### wind speed at 100m (m/s)

## 気圧
### surface air pressure (Pa)

# ある研究[誰によって?]によれば、タクラマカン・ゴビ・黄土高原ともに上空 10 m の平均風速が 5 m/s を超えると、局所的に地面から砂塵が舞い上がり始める。
# [Wikipedia:黄砂](https://ja.wikipedia.org/wiki/%E9%BB%84%E7%A0%82)

# -*- coding: utf-8 -*-
import csv
import os

class YellowSandDataNormalization():

    # 風量データを変換する
    def conversionYellowSandData(self,csvPath):

        # 結果格納用
        editedCsvList = []

        openCsv = open(csvPath, "r")
        csv_reader = csv.reader(openCsv, delimiter=",", quotechar='"')
        dicCsvList = self.conversionDicCsvList(csv_reader)

        tmpDate = ""
        calcDirectionList = []
        calcSpeedList = []
        editedRow = {}

        for row in dicCsvList:

            if tmpDate == "" :
                tmpDate = self.getDate(row)
            elif tmpDate == self.getDate(row) :
                calcDirectionList.append(float(row["direction"]))
                calcSpeedList.append(float(row["speed"]))
            else :
                # 平均化したのを格納する
                editedRow.update({"date":tmpDate})
                editedRow.update({"aveDirection":self.averageValueCalc(calcDirectionList)})
                editedRow.update({"aveSpeed":self.averageValueCalc(calcSpeedList)})
                editedCsvList.append(editedRow)
                editedRow = {}

            # 範囲確認用日付を確保しておく
            tmpDate = self.getDate(row)

        if len(editedCsvList) == 0 and len(calcDirectionList) != 0 and len(calcSpeedList) != 0 :
            # 平均化したのを格納する
            editedRow.update({"date":tmpDate})
            editedRow.update({"aveDirection":self.averageValueCalc(calcDirectionList)})
            editedRow.update({"aveSpeed":self.averageValueCalc(calcSpeedList)})
            editedCsvList.append(editedRow)
            editedRow = {}

        return editedCsvList

    # CSVを辞書型に変換する
    def conversionDicCsvList(self,csv_reader):
        dicCsvList = []
        ExcludedRowCount = 0
        for row in csv_reader:
            # ヘッダ情報を回避する
            if ExcludedRowCount < 4 :
                ExcludedRowCount =  ExcludedRowCount + 1
                continue

            rowTmp = {"Year":row[0],"Month":row[1],"Day":row[2],"Hour":row[3],"Minute":row[4],"power":row[5],"pressure":row[6],"temperature":row[7],"direction":row[8],"speed":row[9]}
            dicCsvList.append(rowTmp)

        return dicCsvList

    # yyyyMMddにフォーマットした日時を取得する
    def getDate(self,rowList):
        yyyyMMdd = rowList["Year"].zfill(4) + rowList["Month"].zfill(2) + rowList["Day"].zfill(2)
        return yyyyMMdd

    # 平均値を計算する
    def averageValueCalc(self,calcList):
        ave = sum(calcList)/len(calcList)
        return ave

    # データの編集を実行する
    def edit(self):

        # 入力フォルダ内の全てのCSVを対象とする
        inputCsvPath = ""
        inputCsvDir = "CSV入力フォルダ"

        # 結果をCSVに出力する
        outputCsvPath = "出力パス/output.csv"
        outputFile = open(outputCsvPath, "a")
        editedCsvLists = []

        files = os.listdir(inputCsvDir)
        for file in files:
            inputCsvPath = inputCsvDir + file
            print(inputCsvPath)
            editedCsvLists.append(self.conversionYellowSandData(inputCsvPath))

        editedCsvList = editedCsvLists[0]
        dictNames = editedCsvList[0].keys()
        csvWriter = csv.DictWriter(outputFile, dictNames)

        for editedCsvList in editedCsvLists:
            for row in editedCsvList:
                csvWriter.writerow(row)

        outputFile.close()

if __name__ == "__main__":

    normalization = YellowSandDataNormalization()
    normalization.edit()
