import numpy as np

moves = {
	'UpLeft': 0,
	'Up': 1,
	'Left': 2,
}


def LCSLength(c, b, x, y):
	for i in range(len(x) + 1):
		c[i, 0] = 0
	for j in range(len(y) + 1):
		c[0, j] = 0
	for i in range(1, len(x) + 1):
		for j in range(1, len(y) + 1):
			if x[i - 1] == y[j - 1]:
				c[i, j] = c[i - 1, j - 1] + 1
				b[i - 1, j - 1] = moves['UpLeft']
			elif c[i - 1, j] >= c[i, j - 1]:
				c[i, j] = c[i - 1, j]
				b[i - 1, j - 1] = moves['Up']
			else:
				c[i, j] = c[i, j - 1]
				b[i - 1, j - 1] = moves['Left']


def printLCS(b, x, i, j):
	if i < 0 or j < 0:
		return
	if b[i, j] == moves['UpLeft']:
		printLCS(b, x, i - 1, j - 1)
		print(x[i])
	elif b[i, j] == moves['Up']:
		printLCS(b, x, i - 1, j)
	else:
		printLCS(b, x, i, j - 1)


def calculate(x, y):
	c = np.full((len(x) + 1, len(y) + 1), -1, int)
	b = np.full((len(x), len(y)), -1, int)
	LCSLength(c, b, x, y)
	print(c)
	print(b)
	print('- LCS Length: ' + str(c[len(x), len(y)]))
	printLCS(b, x, len(x) - 1, len(y) - 1)


def main():
	# x = 'otzaniseinaipaixtaras'
	# y = 'hmariaeinaikouklara'
	x = 'ABCBDAB'
	y = 'BDCABA'
	n = 100
	m = 10
	# np.random.seed(0)
	# x = np.random.randint(0, 26, n)
	# y = np.random.randint(0, 26, m)
	calculate(x, y)


if __name__ == "__main__":
	main()
