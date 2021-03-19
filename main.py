import csv
import os
import time
import traceback
import pprint
from tkinter import filedialog #파일다이어로그
from itertools import groupby #그룹핑
from konlpy.tag import Okt #명사추출
from collections import Counter #단어수총합

#iterable : list dict..등으로 반복가능한 형태 / [] {} 같은 형태 / itor()함수 포함 / for문에 들어가면 자동으로 iterator변환 /
#iterator : next()함수로 반복가능한 객체 / for문에 사용됨 / itor()함수를 이용해 iterable->iterator변환가능 /list(iterator)등올 iterable변형가능

result={} # 결과
resultEtc={} # 기타 결과

def readCsv():
    '''CSV를 읽어서 리스트로 변환한다'''
    global resultEtc #해당함수에서 해당전역변수를 사용하겠다고 선언
    path=filedialog.askopenfilename(initialdir="./resource",filetypes=[("CSV Files", "*.csv")],title="select [ KAKAO TALK CHAT ] file")
    csvLst=[]

    with open(path, newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        #CSV TO LIST
        for idx,row in enumerate(csvReader):
            #시간,이름,메시지 형식이 아닌값을 제거, 첫번째행제거
            if len(row)!=3:
                continue
            if idx==0:
                continue
            csvLst.append(row)

    csvLst.sort(key=lambda x : x[1])#sorted:새롭게배열을만듬 / sort:기존 배열에 저장함 lambda 원소변수명지정:해당원소사용
    resultEtc['lineTotal']=len(csvLst) #총 메시지 수
    
    return csvLst

def checkNoun(csvLst):
    '''명사를 추출한다'''
    global result
    okt = Okt()#konlpy의 라이브러리 
    nounDict = {}
    
    #명사분류
    for idx,row in enumerate(csvLst):
        msgTime=row[0]
        nounMsgList=okt.nouns(row[2])
        # 딕셔너리에 해당하는 키가 존재하면 in 참
        if row[1] in nounDict:
            #nounDict[key[1]].append(list(group_data))#list()형변환 append는 list,dict동일
            nounDict[row[1]].append([msgTime,nounMsgList])#기존추가  [신규블록].append([기존블록])
        else:
            nounDict[row[1]] = [[msgTime,nounMsgList]]#신규추가  [신규블록[기존블록]]
            result[row[1]] ={} #글로벌변수에 사용자 이름 초기 저장
    
    #사용자별 메시지수
    for key,value in nounDict.items():
        result[key]={"총메시지수":len(value)}#1.딕셔너리 생성

    return nounDict
        
def getNounCnt(nounDict):
    '''추출한 명사의 수를 집계한다'''
    global result
    noSearchWord=['사진','동영상','이모티콘','메시지','검색','삭제','샵']

    #사용된 단어 수 집계   #딕셔너리.items() : key,value 둘 다 반환
    for key,value in nounDict.items():
        temp=[]
        #리스트 합치기
        for idx,row in enumerate(value):
            temp.extend(row[1])#list.extend() 리스트합치기
        
        count = Counter(temp)
        cntList=[]#이름넣기
        #명사빈도수찾기
        for n, c in count.most_common(50):
            #1글자이상,검색하지않는단어
            if len(n)>1 and n not in noSearchWord:
                cntList.append({'단어': n, '사용횟수': c})
        
        result[key]["메시지리스트"]=cntList#2.생성된 딕셔너리에 추가

def setUserPercentage():
    '''사용자의 메시지 백분률'''
    global result
    global resultEtc

    for key,value in result.items():
        value['퍼센트']=str(int((value['총메시지수']/resultEtc['lineTotal'])*100))+"%"#int()를사용해서소수점제거

def setKeyKorean():
    result['총메시지수']=result.pop("lineCnt")
    result['메시지리스트']=result.pop("msgList")
    result['횟수']=result.pop("count")
    result['단어']=result.pop("word")
    result['퍼센트']=result.pop("percent")

if __name__=="__main__":
    startTime=time.time()
    try:
        csvLst=readCsv()#CSV를 읽어서 리스트로 변환
        nounDict=checkNoun(csvLst)#명사를 추출
        getNounCnt(nounDict)#추출한 명사의 수를 집계
        setUserPercentage()#사용자의 메시지 백분률
        #setKeyKorean()#딕셔너리의 키를 한국어로 변경
        pprint.pprint(result)#출력

    except Exception as ex:
        print(traceback.print_exc())
    finally:
        print("코드실행시간 ::::: ",time.time()-startTime," :::::")#print(a,b,c) 콤마를 이용해서 문자열과 변수를 같이 출력 

    