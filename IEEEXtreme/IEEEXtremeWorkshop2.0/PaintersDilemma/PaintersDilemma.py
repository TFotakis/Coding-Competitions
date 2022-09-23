# https://csacademy.com/ieeextreme-practice/task/painters-dilemma/

import sys
from fileinput import input as fin
from functools import lru_cache
from itertools import product
import numpy as np

sys.setrecursionlimit(10000)

try:
    f = open('input.txt', 'r')
except:
    f = fin()

c = []


@lru_cache(maxsize=None)
def top_down(index, a, b):
    if index >= len(c):
        return 0
    elif c[index] == a or c[index] == b:
        return top_down(index + 1, a, b)
    else:
        return 1 + min(top_down(index + 1, a, c[index]), top_down(index + 1, c[index], b))
        # return 1 + min(top_down(index + 1, c[index], b), top_down(index + 1, a, c[index]))  # Check correctness


def bottom_up():
    global c

    color_set = set(c + [0])
    d = len(color_set)
    n = len(c)

    # c = list(reversed(c))  # Check if needed

    A = np.zeros((d * d, n + 1), dtype=np.int32)

    color_combs = list(product(sorted(color_set), repeat=2))
    color_comb_dict = {}

    index = 0
    for comb in color_combs:
        color_comb_dict[comb] = index
        index += 1

    for i in range(d * d):
        A[i, 0] = 0

    for j in range(1, n + 1):
        for i in range(d * d):
            state = color_combs[i]
            color = c[j - 1]

            if color in state:
                A[i, j] = A[i, j - 1]
                continue

            stateA = (color, state[1])
            stateB = (state[0], color)
            stateA_index = color_comb_dict[stateA]
            stateB_index = color_comb_dict[stateB]
            A[i, j] = 1 + min(A[stateA_index, j - 1], A[stateB_index, j - 1])

    return A[0, -1]


if __name__ == '__main__':
    t = int(f.readline())
    for _ in range(t):
        n = int(f.readline())
        c = [int(el) for el in f.readline().split()]

        res = bottom_up()
        # res = top_down(0, 0, 0)
        print(res)
        top_down.cache_clear()
