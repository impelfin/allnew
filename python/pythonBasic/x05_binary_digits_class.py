import random

class Binary_digits(object):
	def __init__(self, num, lists):
		self.num = num
		self.lists = lists
	def convert(self):
		q = self.num
		lists = self.lists
		while True:
			r = q % 2
			q = q // 2
			lists.append(r)
			if q == 0:
				break
		lists.reverse()
		return lists

lists = []
num = random.randrange(4, 16)
binary = Binary_digits(num, lists)
print(f'{num} binary number is : {binary.convert()}')


