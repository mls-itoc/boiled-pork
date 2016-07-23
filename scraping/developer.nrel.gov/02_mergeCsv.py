# developer.nrel.govの風データとwww.jma.go.jpの黄砂データをいい感じにマージする
# auther:Mitsuaki Ihara

# -*- coding: utf-8 -*-

import csv

class MergeCsv():

    def merge(self):
        # CSVからデータを取得する
        csvPath = "入力ファイルパス/output.csv"
        openCsv = open(csvPath, "r")
        csv_reader = csv.reader(openCsv, delimiter=",", quotechar='"')
        dicWindCsvList = self.conversionDicWindCsvList(csv_reader)

        csvPath = "入力ファイルパス/yellow_dust.csv"
        openCsv = open(csvPath, "r")
        csv_reader = csv.reader(openCsv, delimiter=",", quotechar='"')
        dicSandCsvList = self.conversionDicSandCsvList(csv_reader)

        # 風力データと黄砂の発生データをマージする
        for row in dicSandCsvList:
            dicWindCsvRow = dicWindCsvList.get(row["date"])
            if dicWindCsvRow is not None:
                dicWindCsvRow.update(row)
                dicWindCsvList.update({row["date"]:dicWindCsvRow})

        # マージしたCSVを出力する
        # ヘッダ情報を取得する
        for key in dicWindCsvList:
            dictNames = dicWindCsvList[key].keys()
            break

        outputCsvPath = "出力ファイルパス/mergeyellowdust.csv"
        outputFile = open(outputCsvPath, "a")
        csvWriter = csv.DictWriter(outputFile, dictNames)

        for key in sorted(dicWindCsvList.keys()):
            print(key)
            csvWriter.writerow(dicWindCsvList[key])
        outputFile.close()


    # 風向きデータを日付単位の辞書付きで変換する
    def conversionDicWindCsvList(self,csv_reader):
        dicWindCsvList = {}

        for row in csv_reader:
            dicWindCsvRow = {}
            # マージのデフォルト値を設定しておく
            rowTmp = {"aveDirection":row[0],"date":row[1],"aveSpeed":row[2],"isYellowDust":"0"}
            dicWindCsvRow.update(rowTmp)
            dicWindCsvList.update({rowTmp["date"]:dicWindCsvRow})
        return dicWindCsvList

    # 黄砂データを日付単位の辞書付きで変換する
    def conversionDicSandCsvList(self,csv_reader):
        dicSandCsvList = []
        ExcludedRowCount = 0

        # ヘッダ情報を回避する必要あり
        for row in csv_reader:

            if ExcludedRowCount < 1 :
                ExcludedRowCount =  ExcludedRowCount + 1
                continue

            rowTmp = {"date":row[1],"isYellowDust":row[2]}
            dicSandCsvList.append(rowTmp)
        return dicSandCsvList

if __name__ == "__main__":
	mergeCsv = MergeCsv()
	mergeCsv.merge()
