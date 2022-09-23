import fileinput as fin

try:
	f = open('input.txt', 'r')
except:
	f = fin.input()


def solve():
	pass


def main():
	try:
		# for _ in range(int(f.readline())):
		print(solve())
	except KeyboardInterrupt:
		print('Save those files')


if __name__ == '__main__':
	main()
