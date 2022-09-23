from .basesolver import BaseSolver
import random

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
		images = {'V': [], 'H': []}
		for i, image in enumerate(self.images):
			images[image['orientation']].append(i)
		horSlides = [[el] for el in images['H']]
		verSlides = []

		score = -1
		while True:
			while images['V']:
				id1 = images['V'][random.randint(0, len(images['V']) - 1)]
				images['V'].remove(id1)
				id2 = images['V'][random.randint(0, len(images['V']) - 1)]
				images['V'].remove(id2)
				verSlides.append([id1, id2])
			slides = horSlides + verSlides

			random.shuffle(slides)
			# self.slides = slides
			# print(slides)
			newScore = self.compute_score_local(slides)
			if newScore > score + 1000:
				score = newScore
				print(self.input_str, ": ", score)
				self.slides = slides
				self.write('output/')

		# return False
