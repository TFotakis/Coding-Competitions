def median(a):
	mid = len(a) // 2
	if len(a) % 2 == 0:
		return (a[mid - 1] + a[mid]) / 2
	return a[mid]


def calculate(a, b):
	k = 0
	while len(a) != 2 and len(b) != 2:
		k += 1
		ma = median(a)
		mb = median(b)
		if ma == mb:
			return ma
		elif ma > mb:
			if len(a) % 2 == 0:
				a = a[:len(a) // 2 + 1]
				b = b[len(b) // 2 - 1:]
			else:
				a = a[:len(a) // 2 + 1]
				b = b[len(b) // 2:]
		else:
			if len(a) % 2 == 0:
				a = a[len(a) // 2 - 1:]
				b = b[:len(b) // 2 + 1]
			else:
				a = a[len(a) // 2:]
				b = b[:len(b) // 2 + 1]
	print(k)
	return (max(a[0], b[0]) + min(a[1], b[1])) / 2


def getMedian(ar1, ar2, n, k=0):
	k += 1
	if n <= 0:
		return -1
	if n == 1:
		print('K:' + str(k))
		return (ar1[0] + ar2[0]) / 2
	if n == 2:
		print('K:' + str(k))
		return (max(ar1[0], ar2[0]) + min(ar1[1], ar2[1])) / 2
	m1 = median(ar1)
	m2 = median(ar2)
	if m1 == m2:
		return m1
	if m1 < m2:
		if n % 2 == 0:
			return getMedian(ar1[n // 2 - 1:], ar2[:n // 2 + 1], n - n // 2 + 1, k)
		return getMedian(ar1[n // 2:], ar2[:n // 2 + 1], n - n // 2, k)
	if n % 2 == 0:
		return getMedian(ar2[n // 2 - 1:], ar1[:n // 2 + 1], n - n // 2 + 1, k)
	return getMedian(ar2[n // 2:], ar1[:n // 2 + 1], n - n // 2, k)


def main(n):
	if n <= 0:
		return -1
	print("N: " + str(n))
	a = list(range(0, 2 * n, 2))
	b = list(range(1, 2 * n + 1, 2))
	c = list(range(0, 2 * n))
	# print(a, b)
	# print(c)
	print('Median: ' + str(median(c)))
	print('Median: ' + str(calculate(a, b)))
	print('Median: ' + str(getMedian(a, b, n)))


if __name__ == "__main__":
	main(10000000)
