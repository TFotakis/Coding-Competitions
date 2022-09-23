import numpy as np


class Color:
	WHITE = 0
	GRAY = 1
	BLACK = 2


def DFSVisit(G, color, d, f, predecessor, time, u):
	color[u] = Color.GRAY
	time += 1
	d[u] = time
	for v in G[u]:
		if color[v] == Color.WHITE:
			predecessor[v] = u
			DFSVisit(G, color, d, f, predecessor, time, v)
	color[u] = Color.BLACK
	time += 1
	f[u] = time


def DFS(G, s):
	color = np.full(shape=len(G), fill_value=Color.WHITE, dtype=int)
	d = np.full(shape=len(G), fill_value=-1, dtype=int)
	f = np.full(shape=len(G), fill_value=-1, dtype=int)
	predecessor = np.full(shape=len(G), fill_value=-1, dtype=int)
	time = 0
	DFSVisit(G, color, d, f, predecessor, time, s)
	# for u in G[s]:
	# 	if color[u] == Color.WHITE:
	# 		DFSVisit(G, color, d, f, predecessor, time, u)
	return predecessor


def TopVisit(G, color, L, u):
	color[u] = Color.GRAY
	for v in G[u]:
		if color[v] == Color.WHITE:
			TopVisit(G, color, L, v)
	color[u] = Color.BLACK
	L.append(u)


def TopSort(G):
	color = np.full(shape=len(G), fill_value=Color.WHITE, dtype=int)
	L = []
	for u in range(len(G)):
		if color[u] == Color.WHITE:
			TopVisit(G, color, L, u)
	return L


def main():
	# G = [[1], [0, 2], [1, 3, 5], [2, 4], [3, 5], [2, 4]]
	clothes = ['shorts', 'socks', 'pants', 'shoes', 'belts', 'shirt', 'tie', 'jacket']
	# G = [[2, 3], [3], [3, 4], [], [7], [4, 6], [7], []]
	G = [[], [], [0], [0, 1, 2], [2, 5], [], [5], [6]]
	# print(DFS(G, 5))
	topSortedIndices = TopSort(G)
	print([clothes[i] for i in topSortedIndices])
	# shortestPath = getShortestPath(G, 4, 1)
	# print(shortestPath)
	# print(whileGetShortestPath(G, 4, 1))


if __name__ == "__main__":
	main()
