import os

filename = "data1.txt"
if os.path.exists(filename):
    os.remove(filename)

f1 = open("data.txt", 'r')
f2 = open("data1.txt", 'w')

for i in range(1, 4):
    line = f1.readline()
    newline = line.replace('AAA', '"BBB"')
    f2.write(newline)
    print(newline)

f1.close()
f2.close()