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

		def printKnapsack(W, wt, val, n):
			selectedItems = []
			K = [[0 for w in range(W + 1)] for i in range(n + 1)]

			# Build table K[][] in bottom
			# up manner
			for i in range(n + 1):
				for w in range(W + 1):
					if i == 0 or w == 0:
						K[i][w] = 0
					elif wt[i - 1] <= w:
						K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
					else:
						K[i][w] = K[i - 1][w]

					# stores the result of Knapsack
			res = K[n][W]
			# print(res)

			w = W
			for i in range(n, 0, -1):
				if res <= 0:
					break
				# either the result comes from the
				# top (K[i-1][w]) or from (val[i-1]
				# + K[i-1] [w-wt[i-1]]) as in Knapsack
				# table. If it comes from the latter
				# one/ it means the item is included.
				if res == K[i - 1][w]:
					continue
				else:
					# This item is included.
					selectedItems.append(i - 1)

					# Since this weight is included
					# its value is deducted
					res = res - val[i - 1]
					w = w - wt[i - 1]
			return selectedItems

		self.PizzasSelected = printKnapsack(self.MaxSlices, self.PizzaSlices, self.PizzaSlices, self.PizzaTypesNum)
		return True
