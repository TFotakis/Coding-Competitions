def calculate(a, i, j):
	if i == j and i == a[i]:
		return i
	mid = int((j - i) / 2) + i
	if mid == a[mid]:
		return mid
	elif mid < a[mid]:
		return calculate(a, 0, mid)
	else:
		return calculate(a, mid + 1, j)


def main():
	# a = [-1, 0, 1, 3]
	a = [-15, -12, -1, 0, 1, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15]
	index = calculate(a, 0, len(a) - 1)
	print(index)


if __name__ == "__main__":
	main()
