# https://csacademy.com/ieeextreme-practice/task/ca9bc49133da9c3c90df045f4ea8fdd3/

import fileinput as fin
import copy

try:
	f = open('input.txt', 'r')
except:
	f = fin.input()


def BFS(graph, s):
	res = []
	queue = [s]
	visited = {v: False for v in graph.keys()}
	visited[s] = True
	while queue:
		v = queue.pop(0)
		res.append(v)

		for u in graph[v]:
			if not visited[u]:
				queue.append(u)
	return res


def winner(matrix):
	for i in range(3):
		if matrix[i][0] == matrix[i][1] == matrix[i][2] == 'x':
			return 1
		if matrix[i][0] == matrix[i][1] == matrix[i][2] == 'o':
			return -1
		if matrix[0][i] == matrix[1][i] == matrix[2][i] == 'x':
			return 1
		if matrix[0][i] == matrix[1][i] == matrix[2][i] == 'o':
			return -1
	if matrix[0][0] == matrix[1][1] == matrix[2][2] == 'x':
		return 1
	if matrix[0][0] == matrix[1][1] == matrix[2][2] == 'o':
		return -1
	if matrix[0][2] == matrix[1][1] == matrix[2][0] == 'x':
		return 1
	if matrix[0][2] == matrix[1][1] == matrix[2][0] == 'o':
		return -1
	return 0


def solve():
	bobList = [(int(el[0]) - 1, int(el[1]) - 1) for el in [f.readline().split() for _ in range(9)]]
	state = {
		'matrix': [
			['.', '.', '.'],
			['.', '.', '.'],
			['.', '.', '.'],
		],
		'path': [],
		'bobsTurn': True,
		'bobsListPos': 0
	}
	queue = [state]
	while queue:
		state = queue.pop(0)
		wins = winner(state['matrix'])
		if wins == -1:
			continue
		if wins == 1:
			return state['path']

		if state['bobsTurn']:
			state['bobsTurn'] = False

			while state['bobsListPos'] < 9:
				y, x = bobList[state['bobsListPos']]
				state['bobsListPos'] += 1
				if state['matrix'][y][x] == '.':
					state['matrix'][y][x] = 'x'
					queue.append(state)
					break
		else:
			for y in range(3):
				for x in range(3):
					if state['matrix'][y][x] == '.':
						newState = copy.deepcopy(state)
						newState['matrix'][y][x] = 'o'
						newState['path'].append([y, x])
						newState['bobsTurn'] = True
						queue.append(newState)


if __name__ == '__main__':
	path = solve()
	res = '\n'.join([' '.join([str(el + 1) for el in cord]) for cord in path])
	print(res)
