from itertools import product
tsn = [str(i) if set(['3', '6', '9']).isdisjoint(set(list(str(i)))) else '👏' if tuple(str(i)) not in list(product(['3', '6', '9'], ['3', '6', '9'])) else '👏👏'  for i in range(1, 101)]
print(tsn)