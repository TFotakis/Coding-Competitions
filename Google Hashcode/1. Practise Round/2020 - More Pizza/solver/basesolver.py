import numpy as np
from tqdm import trange, tqdm


class BaseSolver(object):
	"""Don't touch this!
	This class makes sure that those two methods gets implemented,
	as needed in main.py.
	"""

	def __init__(self, input_str):
		"""Initialization of the given problem."""
		self.MaxSlices = 0
		self.PizzaTypesNum = 0
		self.PizzaSlices = []
		self.PizzasSelected = []

		self.input_str = input_str
		self.read_input()

	def solve(self):
		"""Solves the problem.
		Stores the solution internally.

		:return: True, if a solution is found, False otherwise
		"""
		raise NotImplementedError("This method needs to be implemented.")

	def compute_score(self):
		"""Validates submission and computes score.

		:return: the computed score of the given scheduling
		"""
		sliceCount = 0
		for pizzaIndex in self.PizzasSelected:
			sliceCount += self.PizzaSlices[pizzaIndex]
		return sliceCount

	def write(self, output_str):
		"""Writes a solution file with the solved solution.

		:param output_str: The output filepath where to save the solution.
		:return: Nothing.
		"""
		fileName = self.input_str.split('/')[-1].split('.')[0]
		directory = output_str if output_str[-1] == '/' else output_str + '/'
		path = directory + fileName + '.out'
		with open(path, 'w') as f:
			f.write(str(len(self.PizzasSelected)) + '\n')
			f.write(' '.join([str(el) for el in self.PizzasSelected]))

	def read_input(self):
		with open(self.input_str, 'r') as f:
			[self.MaxSlices, self.PizzaTypesNum] = [int(el) for el in f.readline().split()]
			self.PizzaSlices = [int(el) for el in f.readline().split()]
