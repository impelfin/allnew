import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'

url = "https://movie.daum.net/ranking/reservation"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

infos = soup.findAll('div', attrs={'class':'thumb_cont'})

# print('-' * 40)
# print(infos)
# print('-' * 40)

no = 0
result = []
df = pd.DataFrame()
# print(df)
for info in infos:
    no += 1
    mytitle = info.find('a', attrs={'class':'link_txt'})
    title = mytitle.string
    # print(title)

    a = info.find('span', attrs={'class':'txt_grade'})
    grade = a.string
    # print(grade)

    b = info.find('span', attrs={'class': 'txt_num'}).string.strip('%')
    num = b
    # print(num)

    c = info.find('span', attrs={'class': 'txt_info'})
    d = c.find('span', attrs={'class': 'txt_num'})
    info = d.string
    # print(info)

    result.append([no, title, grade, num, info])
    df = pd.concat([df, pd.DataFrame(result)], axis= 0)
    result = []  #중복값이 안들어갑니다.

df.columns = ['순위', '제목', '평점', '예매율', '개봉일']
df.set_index("제목", inplace=True)
print(df)
print(df.info())
#
# print(result)

newDf =df.loc[:, ['평점','예매율']]
newDf.astype(float).plot(kind='barh', rot=45,legend=True)
plt.title('다음 영화의 평점과 예매율')

filename = 'daummovie.png'
plt.savefig(filename)
print(filename, 'saved ....')
