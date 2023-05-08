import random

def binary_digits(num, lists):
	q = num // 2
	r = num % 2
	lists.append(r)
	if q == 0:
		lists.reverse()
		return lists
	else:
		return binary_digits(q, lists)

lists = []
num = random.randrange(4, 16)
print(f'{num} binary number is : {binary_digits(num, lists)}')


