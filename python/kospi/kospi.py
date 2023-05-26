import json, urllib.request, datetime, math
from urllib.parse import quote

import numpy as np
import pandas as pd
from pandas import Series

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            # print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None
# end def getRequestUrl

def getData(pageNo, numOfRows, basDt, itmsNm):
    end_point = 'http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo'
    #
    # 일반 인증키
    access_key = 'B%2FNiJnYmkZV1%2FK7ulvZI4MoSXvCTDfNAd0Snw%2Bk6g4%2BbMk1LoGVhd75DJahjv4K35Cr9jh9RX0j%2BM89grKBYsw%3D%3D'

    parameters = ''
    parameters += "?resultType=json"
    parameters += "&serviceKey=" + access_key
    parameters += "&pageNo=" + str(pageNo)  # 페이지 번호
    parameters += "&numOfRows=" + str(numOfRows)  # 조회 최대 행수(레코드 수)
    parameters += "&basDt=" + str(basDt)
    parameters += "&itmsNm=" + quote(itmsNm)
    url = end_point + parameters

    # print('URL')
    # print(url)

    result = getRequestUrl(url)
    if (result == None):
        return None
    else:
        return json.loads(result)
# end def getData

basDt = '20230105'
itmsNm = '삼성전자'

jsonResult = []

pageNo = 1  # 페이지 번호
numOfRows = 100  # 조회 레코드(행)의 최대 수
nPage = 0

jsonData = getData(pageNo, numOfRows, basDt, itmsNm)
# print(jsonData)

if (jsonData['response']['header']['resultCode'] == '00'):
    data = jsonData['response']['body']['items']['item']
    myindex = ['기준일자', '단축코드', 'ISIN코드', '종목명', '시장구분', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '상장주식수', '시가총액']
    df = pd.DataFrame(data).T
    df.index = myindex
    print(df)


else:
    print('No Data')