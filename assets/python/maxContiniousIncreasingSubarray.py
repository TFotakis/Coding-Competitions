import numpy as np


def calculateLinear(a):
	counter = 0
	maxCounter = 0
	minIndex = maxIndex = 0
	for i in range(1, len(a)):
		if a[i - 1] <= a[i]:
			counter += 1
			maxIndex = i
		else:
			maxCounter = max(counter + 1, maxCounter)
			counter = 0
			minIndex = maxIndex = i
	print(minIndex)
	print(maxIndex)
	return max(counter + 1, maxCounter)


def findMaxSubArray(a, low, high):
	if low == high:
		return [low, high, 1]

	mid = (low + high) // 2
	[leftLow, leftHigh, leftSum] = findMaxSubArray(a, low, mid)
	[rightLow, rightHigh, rightSum] = findMaxSubArray(a, mid + 1, high)
	[middleLow, middleHigh, middleSum] = findMiddleMaxSubArray(a, low, mid, high)

	if leftSum >= rightSum and leftSum >= middleSum:
		return [leftLow, leftHigh, leftSum]
	elif rightSum >= leftSum and rightSum >= middleSum:
		return [rightLow, rightHigh, rightSum]
	else:
		return [middleLow, middleHigh, middleSum]


def findMiddleMaxSubArray(a, low, mid, high):
	leftLow = rightHigh = mid
	while leftLow >= low and a[leftLow] < a[leftLow + 1]:
		leftLow -= 1
	# for leftLow in range(mid - 1, low - 1, -1):
	# 	if a[leftLow + 1] < a[leftLow]:
	# 		break
	while rightHigh < high and a[rightHigh] < a[rightHigh + 1]:
		rightHigh += 1
	# for rightHigh in range(mid + 1, high + 1):
	# 	if a[rightHigh - 1] > a[rightHigh]:
	# 		break
	return [leftLow, rightHigh, rightHigh - leftLow + 1]


import math


def maxSubArraySum(a, size):
	max_so_far = -math.inf - 1
	max_ending_here = 0

	for i in range(0, size):
		max_ending_here = max_ending_here + a[i]
		if max_so_far < max_ending_here:
			max_so_far = max_ending_here

		if max_ending_here < 0:
			max_ending_here = 0
	return max_so_far


def main(n):
	if n <= 0:
		return -1
	# np.random.seed(0)
	# a = np.random.randint(low=10, size=n)
	# a = list(range(n))
	# n=5
	# a = [0, 1, 2, 3, 4]
	n = 3
	a = [-10, -3, -5]
	# print(a)
	# linear = calculateLinear(a)
	# print(linear)
	# NLogN = findMaxSubArray(a, 0, n - 1)
	# print(NLogN)
	print(maxSubArraySum(a, n))


if __name__ == "__main__":
	main(10)
