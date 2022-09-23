from .basesolver import BaseSolver
import numpy as np
from tqdm import trange, tqdm


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

		capacity = self.MaxSlices
		for k in tqdm(range(self.PizzaTypesNum - 1, -1, -1)):
			if capacity - self.PizzaSlices[k] >= 0:
				self.PizzasSelected.append(k)
				capacity -= self.PizzaSlices[k]
		return True
