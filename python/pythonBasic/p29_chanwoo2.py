tsn = [str(i).replace('3', '👏').replace('6', '👏').replace('9', '👏')  for i in range(1, 101)]
for i, l in enumerate(tsn):
    if '👏' in l:
        print('  ', end='')
        for j in l:
            if j == '👏':
                print('%s'%(j), end='')
        print('\t', end='')
    else:
        print('%6s'%(l), end='')
        print('\t', end='')
    if i % 10 == 9:
        print()
    print('', end='')