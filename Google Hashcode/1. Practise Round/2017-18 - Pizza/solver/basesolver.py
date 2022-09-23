from itertools import permutations

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


class BaseSolver(object):
	"""Don't touch this!
	This class makes sure that those two methods gets implemented,
	as needed in main.py.
	"""

	def __init__(self, input_str):
		"""Initialization of the given problem.
		"""
		self.input_str = input_str
		self.R, self.C, self.L, self.H = 0, 0, 0, 0
		self.pizza = []
		self.slices = []
		self.imgs = []

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
			f.write(str(len(self.slices)))
			# for pizzaSlice in self.slices:
			f.write('\n'.join([' '.join([str(el) for el in pizzaSlice]) for pizzaSlice in self.slices]))
		# f.write('\n')

	def printImage(self):
		img = Image.fromarray(np.array(self.pizza).astype('uint8') * 255)
		img.show()

	def createAllPossibleImagePatterns(self):
		minA = 2 * self.L
		maxA = self.H
		sizes = {}
		for i in range(minA, maxA + 1):
			sizes[i] = []
			for j in range(1, i + 1):
				div = i // j
				if div == i / j and j <= self.R and div <= self.C:
					sizes[i].append((j, div))
		# print(sizes)

		perms = {}

		total = 0
		for a in range(minA, maxA + 1):
			for j in range(self.L, a + 1 - self.L):
				total += 1

		pbar = tqdm(total=total)
		for a in range(minA, maxA + 1):
			perms[a] = set()
			for j in range(self.L, a + 1 - self.L):
				slice_str = ('0' * j) + ('1' * (a - j))
				for p in permutations(slice_str):
					perms[a].add(''.join(p))
				pbar.update(1)
			perms[a] = list(perms[a])
		pbar.close()

		for a in range(minA, maxA + 1):
			for rect in sizes[a]:
				for perm in perms[a]:
					npArr = np.array(list(perm))
					rectArr = npArr.reshape(rect)
					rectImg = rectArr.astype('uint8') * 255
					self.imgs.append(Image.fromarray(rectImg))
		# print(len(self.imgs))
		self.imageRead()

	def imageRead(self):
		pizzaImg = Image.fromarray(np.array(self.pizza).astype('uint8') * 255)
		pImg = cv2.cvtColor(np.asarray(pizzaImg), cv2.COLOR_RGB2BGR)
		method = cv2.TM_SQDIFF_NORMED
		arr = []
		for img in self.imgs:
			patImg = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
			result = cv2.matchTemplate(patImg, pImg, method)
			mn, _, mnLoc, _ = cv2.minMaxLoc(result)
			if mn == 1:
				arr.append([mnLoc, patImg])
				cv2.imshow('pattern', patImg)
				MPx, MPy = mnLoc

				# Step 2: Get the size of the template. This is the same size as the match.
				trows, tcols = patImg.shape[:2]
				pImgTmp = cv2.cvtColor(np.asarray(pizzaImg), cv2.COLOR_RGB2BGR)
				# Step 3: Draw the rectangle on large_image
				cv2.rectangle(pImgTmp, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)

				# Display the original image with the rectangle around the match.
				cv2.imshow('output', pImgTmp)
				cv2.waitKey(0)
			# MPx, MPy = mnLoc
			# trows, tcols = patImg.shape[:2]
			# cv2.rectangle(pImg, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)
			# cv2.imshow('output', pImg)
		# print(result)
		print(arr)
		cv2.destroyAllWindows()

	def imageReadCustom(self):
		pass

	def read_input(self):
		with open(self.input_str, 'r') as f:
			self.R, self.C, self.L, self.H = [int(el) for el in f.readline().split()]
			self.pizza = [[0 if el == 'M' else 1 for el in line] for line in f.readlines()]
			# print(self.pizza)
			# self.printImage()
			self.createAllPossibleImagePatterns()
