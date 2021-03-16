import csv
import os
from tkinter import filedialog
from itertools import groupby

def readCsv():
    path=filedialog.askopenfilename(initialdir="./resource",filetypes=[("CSV Files", "*.csv")],title="select [ KAKAO TALK CHAT ] file")
    with open(path, newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        csvArr=[]

        #csv To array
        for idx,row in enumerate(csvReader):
            if len(row)!=3:
                continue
            if idx==0:
                continue
            csvArr.append(row)
        
        csvArr.sort(key=lambda x : x[1])#sorted:새롭게배열을만듬 sort:기존 배열에 저장함 lambda 원소변수명지정:해당원소사용

        result = {}
        for key, group_data in groupby(csvArr):
            #딕셔너리에 해당하는 키가 존재하면 in 참
            if key[1] in result:
                result[key[1]].append(list(group_data))#list()형변환 append는list,dict동일
            else:
                result[key[1]] = list(group_data)
        print("222222")

if __name__=="__main__":
    readCsv()
    