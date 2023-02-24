# Kuboble solver

This script solves [Kuboble](https://kuboble.com) using a simple breadth first search algorithm.
To use the script, prepare an input file containing the level, the disks and the destinations.

##### Example input file
This is an example of a valid input for level 39. The first line contains the disks (`R`, `G`, `B`) and their associated targets (`@`, `$`, `%`).
Walls are indicated with an `X` and free space with ` ` (a space).
```
R@ G$ B%
XXXXX
XG% X
XR  X
XB@ X
X  $X
XXXXX
```

##### Run the solver
To run the solver, simply invoke it with Python (3.9 or higher) with the file name as an argument:
```shell
python solver.py input.txt
```

It will output a sequence of moves for the optimal solution.