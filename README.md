# local-search-heuristic-simulator

In this project, I investigate Karmarkar's algorithm and other local search heuristic algorithms to obtain approximate solutions across multiple instances of the NP-hard Number Partition problem. I prove correctness and runtime bounds for a dynamic programming algorithm and Karmarkar's algorithm, measure the residue of approximate solutions across different heuristics, and analyze the difference in runtimes. 

---

## Overview

The simulator runs multiple local search algorithms for a random instance of the Number Partition problem, which involves giving signs to each element in a list of numbers such that the absolute value of the sum of all signed elements is minimized; this is defined as the residue.

Karmarkar's algorithm: iteratively takes the differences of the two largest elements until a single element remains

Repeated random: iteratively computes the residues of random solutions and keeps the best one

Hill climbing: only considers neighbors of the current solution in search of lower residue solutions

Simulated annealing: includes temperature parameter that allows the algorithm to pursue a higher residue solution to broaden its search space

Prepartitioning: involves computing a transformation of the original input before running Karmarkar's algorithm in hopes of getting lower-residue solutions

---

## Usage

python partition.py flag algorithm inputfile

flag: for customization
algorithm: numerical label for the type of algorithm to run
0 → Karmarkar's
1 → Repeated Random
2 → Hill Climbing
3 → Simulated Annealing
11 → Prepartitioned Repeated Random
12 → Prepartitioned Hill Climbing
13 → Prepartitioned Simulated Annealing
inputfile: path to file containing input instances

The inputfile should be a list of integers, one per line. The output is the residue obtained by running the specified algorithm with these numbers as input.

Example: Run Karmarkar's algorithm on the inputfile `example_problem_instance.txt`:

python partition.py 0 0 example_problem_instance.txt
Expected output: 813
