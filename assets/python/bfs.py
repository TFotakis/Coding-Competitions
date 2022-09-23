import numpy as np


class Color:
	WHITE = 0
	GRAY = 1
	BLACK = 2


def BFS(G, s):
	color = np.full(shape=len(G), fill_value=Color.WHITE, dtype=int)
	distance = np.full(shape=len(G), fill_value=-1, dtype=int)
	predecessor = np.full(shape=len(G), fill_value=-1, dtype=int)
	color[s] = Color.GRAY
	distance[s] = 0
	Q = [s]
	while len(Q):
		u = Q.pop()
		for v in G[u]:
			if color[v] == Color.WHITE:
				color[v] = Color.GRAY
				distance[v] = distance[u] + 1
				predecessor[v] = u
				Q.append(v)
		color[u] = Color.BLACK
	return predecessor


def calculateShortestPath(predecessor, s, v, shortestPath):
	if v == s:
		shortestPath.append(s)
	elif predecessor[v] != -1:
		calculateShortestPath(predecessor, s, predecessor[v], shortestPath)
		shortestPath.append(v)


def getShortestPath(G, s, v):
	predecessor = BFS(G, s)
	shortestPath = []
	calculateShortestPath(predecessor, s, v, shortestPath)
	return shortestPath


def whileGetShortestPath(G, s, v):
	predecessor = BFS(G, s)
	shortestPath = []
	while predecessor[v] != -1:
		shortestPath.append(v)
		v = predecessor[v]
	if v == s:
		shortestPath.append(v)
	return shortestPath[::-1]


def main():
	G = [[1], [0, 2], [1, 3, 5], [2, 4], [3, 5], [2, 4]]
	shortestPath = getShortestPath(G, 4, 1)
	print(shortestPath)
	print(whileGetShortestPath(G, 4, 1))


if __name__ == "__main__":
	main()
