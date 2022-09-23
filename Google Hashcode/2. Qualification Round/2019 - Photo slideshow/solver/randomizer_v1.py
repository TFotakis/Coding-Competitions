from .basesolver import BaseSolver


class Solver(BaseSolver):
	"""Solve the problem nice and steady!

	!!! This class need to be named 'Solver', otherwise main.py won't find this class.
	"""

	def solve(self):
		"""Compute a solution to the given problem.

		Save everything in an internal state,
		print the calculated score of the solution.

		:return: True, if a solution is found, False otherwise
		"""
		imagesByTags = {}
		for i, image in enumerate(self.images):
			if image['orientation'] == 'V':
				continue

			for tag in image['tags']:
				if tag not in imagesByTags.keys():
					imagesByTags[tag] = []
				imagesByTags[tag].append(i)
		# print(imagesByTags)

		tags = list(imagesByTags.keys())
		tag = tags[0]
		slides = []
		while tags:
			for image in imagesByTags[tag]:
				slides.append(image)
			tags.remove(tag)
			if not tags:
				break
			oldTag = tag
			# print(self.images[self.slides[-1][0]])
			lastSlideTags = self.images[slides[-1]]['tags']
			# print(lastSlideTags)
			for newTag in lastSlideTags:
				if newTag != oldTag:
					if newTag in tags:
						tag = newTag
						break
			if tag == oldTag:
				tag = tags[0]
		# print(list(set(slides)))
		self.slides = [[el] for el in (set(slides))]
		# print(self.slides)
		print(self.input_str, ': ', self.compute_score())

		#
		#
		# maxScore = -1
		# maxId = -1
		# for tag in imagesByTags.keys():
		# 	for image1 in imagesByTags[tag]:
		# 		for image2 in imagesByTags[tag]:
		# 			if image1 == image2:
		# 				continue
		# 			newScore = self.compute_score_per_slide_pair([image1], [image2])
		# 			if maxScore < newScore:
		# 				maxScore = newScore
		# 				maxId = image2
		# 		imagesByTags[tag].remove(image1)
		# 		imagesByTags[tag].remove(maxId)
		#
		return False
