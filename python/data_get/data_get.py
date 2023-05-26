from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import datetime
from dateutil.relativedelta import relativedelta
import urllib
import requests
import pandas as pd
import xmltodict
import json

#before_day = (datetime.date.today() - datetime.timedelta(days=10)).strftime('%Y%m%d')
before_day = (datetime.date.today() - relativedelta(months=1)).strftime('%Y%m%d')
today = datetime.date.today().strftime('%Y%m%d')

key='B%2FNiJnYmkZV1%2FK7ulvZI4MoSXvCTDfNAd0Snw%2Bk6g4%2BbMk1LoGVhd75DJahjv4K35Cr9jh9RX0j%2BM89grKBYsw%3D%3D'
url = f'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={key}&'
queryParams = urlencode({ quote_plus('pageNo') : 1,
                          quote_plus('numOfRows') : 10,
                          quote_plus('startCreateDt') : before_day,
                          quote_plus('endCreateDt') : today})
url2 = url + queryParams

response = urlopen(url2)
results = response.read().decode("utf-8")
results_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(results_to_json))
print(type(data))   # dic
print(data)

corona=data['response']['body']['items']['item']
#추가하고 싶은 리스트 생성
state_dt=[]
decide_cnt=[]
death_cnt=[]
acc_exam_cnt=[]

for i in corona:
    state_dt.append(i['stateDt'])      # stateDt : 20200801 기준일
    decide_cnt.append(i['decideCnt'])  # decideCnt : 14336 확진자 수
    death_cnt.append(i['deathCnt'])    # deathCnt : 75 사망자 수
    acc_exam_cnt.append(i['accExamCnt'])   # accExamCnt : 268212 누적 검사 수

df=pd.DataFrame([state_dt,decide_cnt,death_cnt,acc_exam_cnt]).T
df.columns=['기준일','확진자 수','사망자 수','누적 검사 수']
df=df.sort_values(by='기준일', ascending=True)

# csv 파일 생성
df.to_csv('sample.csv')
# 메모장
df.to_csv('sample.txt')
