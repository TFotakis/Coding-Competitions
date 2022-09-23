import numpy as np
import time

start_time = time.time()
end_time = time.time() - start_time

np.random.seed(0)

A = np.random.randint(10, size=(10, 100000))
B = np.random.randint(10, size=(100000, 5))
C = np.random.randint(10, size=(5, 5000))


def matrixMultiply(A, B):
	if A.ndim != 2 or B.ndim != 2 or A.shape[1] != B.shape[0]:
		print("Incompatible arrays")
		return
	C = np.zeros((A.shape[0], B.shape[1]), int)
	for i in range(A.shape[0]):
		for j in range(B.shape[1]):
			for k in range(A.shape[1]):
				C[i, j] = C[i, j] + A[i, k] * B[k, j]
	return C


def numpyMatrixMultiply(A, B):
	return np.mat(A) * np.mat(B)


def naiveMatrixMultiply(A, B):
	return A @ B


if __name__ == "__main__":
	pass
