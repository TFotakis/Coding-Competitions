import fileinput as fin

try:
	f = open('input.txt', 'r')
except:
	f = fin.input()


def solve():
	s, m, r, b = [int(el) for el in f.readline().split()]
	arr = [m, r, b]

	arr = sorted(arr, reverse=True)
	arr[0] -= arr[1]
	tacos = arr[1]
	arr[1] = 0

	arr = sorted(arr, reverse=True)
	arr[0] -= arr[1]
	tacos += arr[1]
	arr[1] = 0

	return min(s, tacos)


if __name__ == '__main__':
	for _ in range(int(f.readline())):
		print(solve())
