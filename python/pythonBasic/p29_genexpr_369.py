numbers = (i for i in range(1, 101))

data = list(numbers)

item = [3, 6, 9]

for i in data:
    n10 = int(i / 10)
    n1 = i % 10
    if i % 10 == 1:
        print()
    if i < 10:
        if i in item:
            print('  👏', end="")
        else:
            print("%4d" % i, end="")
    else:
        if n10 in item and n1 in item:
            print(' 👏👏', end="")
        elif n10 in item or n1 in item:
            print('  👏', end="")
        else:
            print("%4d" % i, end="")