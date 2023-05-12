import urllib.request
from bs4 import BeautifulSoup
from pandas import DataFrame

url = "https://movie.daum.net/ranking/reservation"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

infos = soup.findAll('div', attrs={'class':'thumb_cont'})
print('-' * 40)
print(infos)
print('-' * 40)

no = 0
result = []
for info in infos:
    no += 1
    mytitle = info.find('a', attrs={'class':'link_txt'})
    title = mytitle.string
    print(title)