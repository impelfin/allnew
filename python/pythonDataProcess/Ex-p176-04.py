from pandas import DataFrame

sdata = {
    '국어' : [40, 60, 80, 50, 30],
    '영어' : [55, 65, 75, 85, 60],
    '수학' : [30, 40, 50, 60, 70]
}

myindex = ['강감찬', '이순신','김유신','김구','안중근']
myframe = DataFrame(sdata, index=myindex)
print(myframe)

print('\n짝수 행만 읽어보세요.')
result = myframe.iloc[0::2]
print(result)

print('\n이순신 행만 시리즈로 읽어보세요.')
result = myframe.loc[['이순신']]
print(result)

print('\n강감찬의 영어 점수를 읽어보세요.')
result = myframe.loc[['강감찬'],['영어']]
print(result)

print('\n안중근과 강감찬의 국어/수학 점수를 읽어보세요.')
result = myframe.loc[['안중근', '강감찬'],['국어','수학']]
print(result)

print('\n이순신과 강감찬의 영어 점수를 80으로 변경하세요.')
result = myframe.loc[['이순신', '강감찬'],['영어']] = 80
print(myframe)

print('\n이순신부터 김구까지 수학 점수를 100으로 변경하세요.')
result = myframe.loc['이순신':'김구','수학'] = 100
print(myframe)
