class Graph:
	def __init__(self, graphDict=None):
		if graphDict is None:
			graphDict = {}
		self.__graphDict = graphDict
		self.__weightsDict = None
		self.__distance = [None for _ in self.vertices]
		self.__parent = [None for _ in self.vertices]

	@property
	def vertices(self):
		return list(self.__graphDict.keys())

	@property
	def V(self):
		return self.vertices

	def __generateEdges(self):
		edges = []
		for vertex in self.__graphDict:
			for neighbour in self.__graphDict[vertex]:
				if (vertex, neighbour) not in edges:
					edges.append((vertex, neighbour))
		return edges

	@property
	def edges(self):
		return self.__generateEdges()

	@property
	def E(self):
		return self.edges

	@property
	def weight(self):
		return self.__weightsDict

	@property
	def w(self):
		return self.__weightsDict

	@property
	def distance(self):
		return self.__distance

	@property
	def d(self):
		return self.__distance

	@property
	def parents(self):
		return self.__parent

	@property
	def p(self):
		return self.__parent

	@property
	def pred(self):
		return self.__parent

	def addVertex(self, vertex):
		if vertex not in self.__graphDict:
			self.__graphDict[vertex] = []

	def addEdge(self, edge):
		edge = set(edge)
		(vertex1, vertex2) = tuple(edge)
		if vertex1 in self.__graphDict:
			self.__graphDict[vertex1].append(vertex2)
		else:
			self.__graphDict[vertex1] = [vertex2]

	def addWeights(self, weightsDict=None):
		if weightsDict is None:
			weightsDict = {}
		if self.__weightsDict is None:
			self.__weightsDict = weightsDict
		else:
			for edge, weight in weightsDict.items():
				self.__weightsDict[edge] = weight

	def edgesStartingFromVertex(self, vertex):
		return self.__graphDict[vertex]

	def __str__(self):
		res = 'Vertices: '
		for vertex in self.vertices:
			res += str(vertex) + ' '
		res += '\nEdges: '
		for edge in self.edges:
			res += str(edge) + ' '
		if self.__weightsDict is not None:
			res += '\nWeights: '
			for edge, weight in self.__weightsDict.items():
				res += str(edge) + ': ' + str(weight) + ' '
		return res


def MinDijkstra(G, s):
	visited = {s: 0}
	path = {}
	nodes = G.vertices
	while nodes:
		minNode = None
		for node in nodes:
			if node in visited:
				if minNode is None:
					minNode = node
				elif visited[node] < visited[minNode]:
					minNode = node
		if minNode is None:
			break
		nodes.remove(minNode)
		currentWeight = visited[minNode]
		for edge in G.edgesStartingFromVertex(minNode):
			weight = currentWeight + G.weight[(minNode, edge)]
			if edge not in visited or weight < visited[edge]:
				visited[edge] = weight
				path[edge] = minNode
	return visited, path


def MaxDijkstra(G, s):
	visited = {s: 0}
	path = {}
	nodes = set(G.vertices)
	while nodes:
		maxNode = None
		for node in nodes:
			if node in visited:
				if maxNode is None:
					maxNode = node
				elif visited[node] > visited[maxNode]:
					maxNode = node
		if maxNode is None:
			break
		nodes.remove(maxNode)
		currentWeight = visited[maxNode]
		for edge in G.edgesStartingFromVertex(maxNode):
			weight = G.weight[(maxNode, edge)]
			# weight = currentWeight + G.weight[(maxNode, edge)]
			if edge not in visited or weight > visited[edge]:
				visited[edge] = weight
				path[edge] = maxNode
	return visited, path


def getMinPath(G, u, v):
	visited, graph = MinDijkstra(G, u)
	prev = graph[v]
	path = [v]
	while prev != u:
		path.append(prev)
		prev = graph[prev]
	path.append(u)
	return path[::-1]


def getMaxBandwidthPath(G, u, v):
	"""
	:returns the path with the biggest edge weights so
	that minimum bottlenecking is achieved (every weight can
	be considered as the edge's bandwidth)
	"""
	visited, graph = MaxDijkstra(G, u)
	prev = graph[v]
	path = [v]
	while prev != u:
		path.append(prev)
		prev = graph[prev]
	path.append(u)
	for weight, value in G.weight.items():
		G.weight[weight] = -1 * value
	return path[::-1]


def main():
	graphDict = {
		's': ['t', 'y'],
		't': ['y', 'x'],
		'y': ['t', 'x', 'z'],
		'x': ['z'],
		'z': ['s', 'x']
	}
	G = Graph(graphDict)
	weightsDict = {
		('s', 't'): 10,
		('s', 'y'): 5,
		('t', 'y'): 2,
		('t', 'x'): 1,
		('y', 't'): 3,
		('y', 'x'): 9,
		('y', 'z'): 2,
		('x', 'z'): 4,
		('z', 's'): 7,
		('z', 'x'): 6,
	}
	G.addWeights(weightsDict)

	print(getMinPath(G, 's', 'y'))
	print(getMaxBandwidthPath(G, 'y', 't'))


if __name__ == "__main__":
	main()
