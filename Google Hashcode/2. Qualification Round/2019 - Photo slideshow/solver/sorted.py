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
		images = sorted(self.images, key=lambda x: len(x['tags']))

