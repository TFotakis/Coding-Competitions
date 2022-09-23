import numpy as np
import time


def lookupChain(p, m, s, i, j):
	if m[i, j] != np.Inf:
		return m[i, j]
	if i == j:
		m[i, j] = 0
		return 0
	for k in range(i, j):
		q1 = lookupChain(p, m, s, i, k)
		q2 = lookupChain(p, m, s, k + 1, j)
		q3 = p[i] * p[k + 1] * p[j + 1]
		q = q1 + q2 + q3
		if q < m[i, j]:
			m[i, j] = q
			s[i, j] = k
	return m[i, j]


def printOptPar(s, i, j):
	if i == j:
		print('A' + str(i), end='')
	else:
		print('(', end='')
		printOptPar(s, i, s[i, j])
		print(' * ', end='')
		printOptPar(s, s[i, j] + 1, j)
		print(')', end='')


def memoizedMatrixChain(p):
	print('\nMemoized Matrix Chain')
	n = len(p) - 1
	m = np.full((n, n), np.Inf)
	s = np.full((n, n), -1)
	start_time = time.time()
	lookupChain(p, m, s, 0, n - 1)
	print('- Time Needed (ms): ' + str((time.time() - start_time) * 1000))
	print('- Solution: ', end='')
	printOptPar(s, 0, n - 1)
	print("\n")


def matrixChainOrder(p):
	print('Matrix Chain Order')
	n = len(p) - 1
	m = np.full((n, n), np.Inf)
	s = np.full((n, n), -1)
	start_time = time.time()
	for i in range(n):
		m[i, i] = 0
	for l in range(2, n + 1):
		for i in range(n - l + 1):
			j = i + l - 1
			for k in range(i, j):
				q1 = m[i, k]
				q2 = m[k + 1, j]
				q3 = p[i] * p[k + 1] * p[j + 1]
				q = q1 + q2 + q3
				if q < m[i, j]:
					m[i, j] = q
					s[i, j] = k
	print('- Time Needed (ms): ' + str((time.time() - start_time) * 1000))
	print('- Solution: ', end='')
	printOptPar(s, 0, n - 1)


def main():
	p = [10, 100, 5, 50]
	# p = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
	# p = np.concatenate((p, p))
	memoizedMatrixChain(p)
	matrixChainOrder(p)


if __name__ == "__main__":
	main()
