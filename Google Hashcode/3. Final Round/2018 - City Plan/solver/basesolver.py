import numpy as np
from tqdm import trange, tqdm


class BaseSolver(object):
	"""Don't touch this!
	This class makes sure that those two methods gets implemented,
	as needed in main.py.
	"""

	def __init__(self, input_str):
		"""Initialization of the given problem.
		"""
		# Add your own data
		self.DummyData = None
		self.DummyCharacteristics = None

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
		pass

	def write(self, output_str):
		"""Writes a solution file with the solved solution.

		:param output_str: The output filepath where to save the solution.
		:return: Nothing.
		"""
		fileName = self.input_str.split('/')[-1].split('.')[0]
		directory = output_str if output_str[-1] == '/' else output_str + '/'
		path = directory + fileName + '.out'
		with open(path, 'w') as f:
			# Todo: Write your own format
			f.write(str(self.DummyData))
			f.write('\n'.join([' '.join([str(el) for el in obj]) for obj in self.DummyData]))

	def read_input(self):
		with open(self.input_str, 'r') as f:
			# Todo: Read your own format
			self.DummyCharacteristics = [int(el) for el in f.readline().split()]
			self.DummyData = [[0 if el == 'something' else 1 for el in line] for line in f.readlines()]
