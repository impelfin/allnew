from itertools import count
from ChickenUtil import ChickenStore

###########################################
brandName = 'pelicana' # 브랜드 이름
base_url = 'https://www.pelicana.co.kr/store/stroe_search.html'  # 접속 url
###########################################

def getData():
    savedData = [] # 엑셀로 저장할 리스트
    
    for page_idx in count():
        url = base_url + '?page=' + str(page_idx + 1)
        # print( url )
        chknStore = ChickenStore(brandName, url)
        soup = chknStore.getSoup()

        mytable = soup.find('table', attrs={'class':'table mt20'})
        mytbody = mytable.find('tbody')
        # print(mytbody)

        shopExists = False # 매장 목록이 없다고 가정
        for mytr in mytbody.findAll('tr'):
            shopExists = True
            mylist = list(mytr.strings)
            # print(mylist)

            imsiphone = mytr.select_one('td:nth-of-type(3)').string
            if imsiphone != None:
                phone = imsiphone.strip()
            else:
                phone = ""

            store = mylist[1]
            address = mylist[3]

            if len(address) >= 2:
                imsi = address.split()
                sido = imsi[0]
                gungu = imsi[1]

            mydata = [brandName, store, sido, gungu, address, phone]
            print(mydata)
            savedData.append(mydata)

        if shopExists == False :
            chknStore.save2Csv(savedData)
            break

###########################################
print(brandName + ' 매장 크롤링 시작')
getData()
print(brandName + ' 매장 크롤링 끝')
