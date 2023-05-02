numbers = (i for i in range(1, 101))
clap = "👏"
numbers = list(numbers)

three_six_nine = [3, 6, 9]

for i in numbers:
    if i % 10 in three_six_nine and int(i / 10) in three_six_nine:
        numbers[i-1] = clap + clap
    elif i % 10 in three_six_nine or int(i / 10) in three_six_nine:
        numbers[i-1] = clap

for i in range(len(numbers)):
    n10 = int((i + 1) / 10)
    n1 = (i+1) % 10
    if n1 == 0 and n10 != 0:
        print(numbers[i])
    else :
        if type(numbers[i]) == int:
            print("%2d" % numbers[i] , end=" ")
        else :
            print(numbers[i], end =" ")
