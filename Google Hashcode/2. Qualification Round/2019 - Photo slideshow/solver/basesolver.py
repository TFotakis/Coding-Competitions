class BaseSolver(object):
	"""Don't touch this!
	This class makes sure that those two methods gets implemented,
	as needed in main.py.
	"""

	def __init__(self, input_str):
		"""Initialization of the given problem.
		"""
		# Add your own data
		self.N = 0
		self.images = []
		self.slides = []
		# self.slides = [[0], [3], [1, 2]]

		self.input_str = input_str
		self.read_input()

	def solve(self):
		"""Solves the problem.
		Stores the solution internally.

		:return: True, if a solution is found, False otherwise
		"""
		raise NotImplementedError("This method needs to be implemented.")

	def compute_score_per_slide_pair(self, slide1, slide2):
		tags1 = set(self.images[slide1[0]]['tags'] if len(slide1) == 1 else self.images[slide1[0]]['tags'] + self.images[slide1[1]]['tags'])
		tags2 = set(self.images[slide2[0]]['tags'] if len(slide2) == 1 else self.images[slide2[0]]['tags'] + self.images[slide2[1]]['tags'])
		# print('Slide1 tags: ', tags1)
		# print('Slide2 tags: ', tags2)
		combinedTags = set(list(tags1) + list(tags2))
		# print('Combined tags: ', combinedTags)
		tags1Len = len(tags1)
		tags2Len = len(tags2)
		combinedTagsLen = len(combinedTags)
		commonTagsNumber = tags1Len + tags2Len - combinedTagsLen

		slide1NonCommon = tags1Len - commonTagsNumber
		slide2NonCommon = tags2Len - commonTagsNumber
		# print('Common Tags Number: ', commonTagsNumber)
		# print('Slide1 non-common tags: ', slide1NonCommon)
		# print('Slide2 non-common tags: ', slide2NonCommon)

		return min(commonTagsNumber, slide1NonCommon, slide2NonCommon)

	def compute_score_local(self, slides):
		score = 0
		for i in range(len(slides) - 1):
			score += self.compute_score_per_slide_pair(slides[i], slides[i + 1])
		return score

	def compute_score(self):
		"""Validates submission and computes score.

		:return: the computed score of the given scheduling
		"""
		score = 0
		for i in range(len(self.slides) - 1):
			score += self.compute_score_per_slide_pair(self.slides[i], self.slides[i + 1])
		return score

	def write(self, output_str):
		"""Writes a solution file with the solved solution.

		:param output_str: The output filepath where to save the solution.
		:return: Nothing.
		"""
		fileName = self.input_str.split('/')[-1].split('.')[0]
		directory = output_str if output_str[-1] == '/' else output_str + '/'
		path = directory + fileName + '.out'
		with open(path, 'w') as f:
			# Write your own format
			f.write(str(len(self.slides)) + '\n')
			f.write('\n'.join([' '.join([str(el) for el in obj]) for obj in self.slides]))

	def read_input(self):
		with open(self.input_str, 'r') as f:
			self.N = int(f.readline())
			# print("N ", self.N)
			for i in range(self.N):
				line = f.readline().split()
				orientation, ntags, tags = line[0], int(line[1]), line[2:]
				self.images.append({
					'orientation': orientation,
					'ntags': ntags,
					'tags': tags
				})
		# print(self.images)
