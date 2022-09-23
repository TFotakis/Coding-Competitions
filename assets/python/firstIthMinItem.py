import numpy as np


def median(a):
	mid = len(a) // 2
	if len(a) % 2 == 0:
		return (a[mid - 1] + a[mid]) / 2
	return a[mid]


def getMedianOfUnsortedArray(a):
	"""We suppose this function runs in O(1) and we use it as a black box"""
	a = np.array(a).sort()
	return median(a)


count = 0


def l1(a, pivot):
	if len(a) == 0:
		return a
	b = []
	for i in range(len(a)):
		if a[i] > pivot:
			b.append(a[i])
	return b


def l2(a, pivot):
	if len(a) == 0:
		return a
	b = []
	for i in range(len(a)):
		if a[i] < pivot:
			b.append(a[i])
	return b


def select5(a, k):
	global count
	count += 1
	n = len(a)
	if n <= 10:
		arr = np.array(a)
		arr.sort()
		return arr[k - 1]
	m = n // 5
	list = []
	x = []
	for i in range(m):
		arr = np.array(a[i * 5: i * 5 + 5])
		arr.sort()
		list.append(arr)
		x.append(arr[2])
	if len(x) == 1:
		v = x[0]
	else:
		v = select5(x, len(x) // 2)
	l = l2(a, v)
	r = l1(a, v)
	if k == len(l) + 1:
		return v
	elif k <= len(l):
		return select5(l, k)
	else:
		return select5(r, k - len(l) - 1)


def main(n, i):
	if n <= 0:
		return -1
	np.random.seed(0)
	a = np.random.randint(low=100, size=n)
	# a = [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]
	aSorted = np.sort(a)
	print(str(i) + '-th smallest element is: ' + str(aSorted[i - 1]))
	print(np.array([list(range(n)), aSorted, a]))
	print(select5(a, i))
	print('Count: ' + str(count))


if __name__ == "__main__":
	main(10, 7)
