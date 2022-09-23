import numpy as np


def fillSack(value, weight, W):
	M = np.zeros((len(value) + 1, W + 1), int)
	for i in range(1, len(value) + 1):
		for w in range(1, W + 1):
			if weight[i - 1] > w:
				M[i, w] = M[i-1, w]
			else:
				M[i, w] = max(M[i-1, w], value[i - 1] + M[i - 1, w - weight[i - 1]])
	return M


def getSelectedItems(value, weight, W, M):
	selectedItems = []
	i = len(value)
	w = W
	while i > 0 and w > 0:
		if M[i, w] == M[i-1, w]:
			i = i - 1
		else:
			selectedItems.append(i - 1)
			i = i - 1
			w = w - weight[i]
	return selectedItems[::-1]


def main():
	v = [1, 6, 18, 22, 28]
	w = [1, 2, 5, 6, 7]
	W = 11
	M = fillSack(v, w, W)
	print(M)
	selectedItems = getSelectedItems(v, w, W, M)
	selectedValues = [v[index] for index in selectedItems]
	print(selectedValues)


if __name__ == "__main__":
	main()
