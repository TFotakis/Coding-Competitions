# Google Hashcode 2020 - Practice Round - More Pizza
## Score
Input | Score
--- | ---
A - example | 16 (Max theoretical)
B - small | 100 (Max theoretical)
C - medium | 4500 (Max theoretical)
D - quite big | 999,999,725
E - also big | 504,999,983
Total score | 1,505,004,324
Total theoretical max | 1,505,004,616
Total Loss | 292

There are two solvers, solver/sorting.py and solver/knapsack.py.   
When the memory footprint needed for using the Knapsack solver exceeds 8GB of RAM, the simple sorting solver is being used. This optimizes the solutions for small inputs like input/a_example.in, input/b_small.in and input/c_medium.in.

Any suggestions for other solvers with better scoring for the big inputs, D and E, are welcome.
