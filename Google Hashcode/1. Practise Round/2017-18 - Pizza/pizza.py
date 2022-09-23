# Test round
# Tested on Python 3.5.3
#

import math
import os
import sys

import numpy as np
import tqdm


class Pizza:
    def __init__(self, pizza, R, C, L, H, name):
        self.slices = []
        self.pizza = pizza
        self.R = R  # Rows
        self.C = C  # Columns
        self.L = L  # Min number of each ingredient per slice
        self.H = H  # Max cells per slice
        self.name = name

    def checkInside(self, R, C):  # Safety check for OutOfBounds Exception. Very fast method.
        return 0 <= R[0] < self.R and 0 <= C[0] < self.C and \
               0 <= R[1] < self.R and 0 <= C[1] < self.C

    def checkH(self, R, C):  # Prevent the slice to include cells of other slices.
        if self.checkInside(R, C):
            curSlice = self.pizza[R[0]:R[1] + 1, C[0]:C[1] + 1]
            if curSlice.size <= self.H and not math.isnan(curSlice.sum()):
                return True
        return False

    def checkL(self, R, C):
        cur_slice = self.pizza[R[0]:(R[1] + 1), C[0]:(C[1] + 1)]  # slice of pizza
        tomatoes = np.sum(cur_slice)
        mushrooms = np.size(cur_slice) - tomatoes
        return tomatoes >= self.L and mushrooms >= self.L

    def bigger_slice(self, R, C, direction):  # (R)ight,(L)eft,(D)own,(U)p
        global nextDir
        advanceRow = list(R)
        advanceCol = list(C)

        if direction == 'L':
            advanceCol[0] -= 1
            nextDir = 'U'
        elif direction == 'R':
            advanceCol[1] += 1
            nextDir = 'D'
        elif direction == 'U':
            advanceRow[0] -= 1
            nextDir = 'R'
        elif direction == 'D':
            advanceRow[1] += 1
            nextDir = 'L'

        return advanceRow, advanceCol, nextDir

    def newSlice(self, point):
        # Take a point and returns a slice if possible.The returned slice is defined by lists R and C
        row_final = [point[0], point[0]]
        col_final = [point[1], point[1]]
        direction = 'R'  # Start exploring to the right

        done = False
        while not done:
            passH = False
            counter = 0
            while counter <= 2:
                # Try enlarge the slice
                advRow, advCol, direction = self.bigger_slice(row_final, col_final, direction)
                if self.checkH(advRow, advCol):
                    passH = True
                    row_final = advRow
                    col_final = advCol
                    break
                counter += 1
            if not passH:  # Stop when H cant be satisfied
                done = True

        success = self.checkL(row_final, col_final)
        return success, row_final, col_final

    def start(self):
        # Try to generate a slice from each cell of the pizza
        for row in tqdm.tqdm(range(self.R), desc=self.name):
            for col in range(self.C):
                if not math.isnan(self.pizza[row][col]):  # Don't revisit 'eaten' slices
                    success, R, C = self.newSlice([row, col])
                    if success:
                        self.slices += [[R[0], C[0], R[1], C[1]]]
                        curSlice = np.empty([R[1] - R[0] + 1, C[1] - C[0] + 1])
                        curSlice[:] = None
                        self.pizza[R[0]:R[1] + 1, C[0]:C[1] + 1] = curSlice


if __name__ == '__main__':
    InputFolder = ''
    OutputFolder = ''

    if len(sys.argv) < 3:
        InputFolder = 'inputPizza'  # Reads all the files inside this folder
        OutputFolder = 'output'  # Same names as input
    else:
        InputFolder = sys.argv[1]
        OutputFolder = sys.argv[2]

    if not os.path.exists(InputFolder):
        print('The given input folder argument is invalid..')
        sys.exit(-1)

    for pizza_name in os.listdir(InputFolder):
        pizza_path = os.path.join(InputFolder, pizza_name)

        with open(pizza_path, 'r') as file:
            line = file.readline()
            R, C, L, H = [int(n) for n in line.split()]

            pizza = np.zeros([R, C])
            for row in range(R):
                for ingredient, col in zip(file.readline(), range(C)):
                    if ingredient == 'T':  # Return the pizza as a binary matrix: Tomatoes = 1, Mushrooms = 0
                        pizza[row, col] = 1
                    else:
                        pizza[row, col] = 0

            pizzaRes = Pizza(pizza, R, C, L, H, pizza_name)
            pizzaRes.start()
            output_path = os.path.join(OutputFolder, pizza_name.replace('.in', '.out'))

            if not os.path.exists(OutputFolder):
                os.makedirs(OutputFolder)

            with open(output_path, 'w') as file:
                file.write('{}\n'.format(len(pizzaRes.slices)))
                for _slice in pizzaRes.slices:
                    file.write(' '.join([str(item) for item in _slice]) + '\n')
