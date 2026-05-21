import sys
import random
import math

# List-based implementation of a binary max heap
class BinaryMaxHeap:
    def __init__(self):
        self.arr = []
        self.size = 0

    def get_left(self, i):
        return 2*i + 1

    def get_right(self, i):
        return 2*i + 2

    def get_parent(self, i):
        return (i-1)//2

    def peek_max(self):
        if self.size > 0:
            return self.arr[0]
        else:
            return None

    def _swap(self, i, j):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def _max_heapify_up(self, i): 
        # Boils a node (ideally a leaf) up until it is no longer greater than its parent
        while i > 0 and self.arr[self.get_parent(i)] < self.arr[i]:
            parent_idx = self.get_parent(i)
            self._swap(i, parent_idx)
            i = parent_idx

    def _max_heapify_down(self, i): 
        # Pushes a node (ideally a root) down until it is no longer smaller than its children
        largest_idx = i
        left_idx = self.get_left(i)
        right_idx = self.get_right(i)

        if left_idx < self.size and self.arr[largest_idx] < self.arr[left_idx]:
            largest_idx = left_idx
        if right_idx < self.size and self.arr[largest_idx] < self.arr[right_idx]:
            largest_idx = right_idx
        
        if largest_idx != i:
            self._swap(i, largest_idx)
            self._max_heapify_down(largest_idx)

    def extract_max(self):
        if self.size == 0:
            raise IndexError("Heap is already empty")
        
        max_element = self.arr[0]
        self._swap(0, -1)
        self.size -= 1
        self.arr.pop()
        if self.size > 0:
            self._max_heapify_down(0)

        return max_element
    
    def insert(self, val):
        self.size += 1
        self.arr.append(val)
        self._max_heapify_up(self.size - 1)

        return val

# Algorithm implementations
def karmarkar_karp(num_list):
    maxheap = BinaryMaxHeap()
    for num in num_list:
        maxheap.insert(num)

    # Run the iterative process for Karmarkar
    for i in range(len(num_list) - 1):
        highest = maxheap.extract_max()
        second_highest = maxheap.extract_max()
        diff = highest - second_highest
        maxheap.insert(diff)

    res = maxheap.peek_max()
    return res

def repeated_random(num_list, num_iter):
    min_residue = sum(num_list)
    num_elements = len(num_list)

    # Exhaustively look for random improvements
    for _ in range(num_iter):
        sign_sequence = [random.choice([-1, 1]) for _ in range(num_elements)]
        sign_sum = 0

        for i in range(num_elements):
            sign_sum += sign_sequence[i] * num_list[i]

        residue = abs(sign_sum)
        min_residue = min(min_residue, residue)

    return min_residue

def hill_climbing(num_list, num_iter):
    num_elements = len(num_list)

    # Calculate initial solution, initial residue
    cur_soln = [random.choice([-1, 1]) for _ in range(num_elements)]
    
    sign_sum = 0
    for i in range(num_elements):
        sign_sum += cur_soln[i] * num_list[i]
    
    cur_residue = abs(sign_sum)

    for _ in range(num_iter):
        # Get random neighbor
        i, j = random.sample(range(num_elements), 2)
        neighbor_soln = cur_soln
        neighbor_soln[i] *= -1
        neighbor_soln[j] *= random.choice([-1, 1])

        # Compute the residue of random neighbor
        neighbor_sign_sum = 0
        for k in range(num_elements):
            neighbor_sign_sum += neighbor_soln[k] * num_list[k]
        neighbor_residue = abs(neighbor_sign_sum)

        if neighbor_residue < cur_residue:
            cur_residue = neighbor_residue
            cur_soln = neighbor_soln

    return cur_residue

def simulated_annealing(num_list, num_iter):
    num_elements = len(num_list)

    # Start with random solution
    cur_soln = [random.choice([-1, 1]) for _ in range(num_elements)]

    # Calculate initial residue
    sign_sum = 0
    for i in range(num_elements):
        sign_sum += cur_soln[i] * num_list[i]
    cur_residue = abs(sign_sum)
    min_residue = cur_residue

    for t in range(num_iter):
        # Generate random neighbor
        i, j = random.sample(range(num_elements), 2)
        neighbor_soln = cur_soln
        neighbor_soln[i] *= -1
        neighbor_soln[j] *= random.choice([-1, 1])

        # Compute residue of random neighbor
        neighbor_sign_sum = 0
        for k in range(num_elements):
            neighbor_sign_sum += neighbor_soln[k] * num_list[k]
        neighbor_residue = abs(neighbor_sign_sum)

        if neighbor_residue < cur_residue:
            cur_soln = neighbor_soln
            cur_residue = neighbor_residue
        else:
            # Add random chance that we set neighbor to be current solution 
            prob = math.exp(-1 * (neighbor_residue - cur_residue) / (t_cooling(t)))
            if random.uniform(0,1) < prob:
                cur_soln = neighbor_soln
                cur_residue = neighbor_residue

        # Replace best-residue solution with current solution if it truly improves residue
        if cur_residue < min_residue:
            min_residue = cur_residue
    
    return min_residue

def prepartitioned_repeated_random(num_list, num_iter):
    num_elements = len(num_list)
    max_residue = sum(num_list)
    p_seq = [random.randint(0, num_elements-1) for _ in range(num_elements)]

    # Get the alternate representation of the input sequence
    prepartitioned_num_list = [0] * num_elements
    for j in range(num_elements):
        prepartitioned_num_list[p_seq[j]] += num_list[j]

    # Get the initial residue of the solution coming from prepartition
    min_residue = karmarkar_karp(prepartitioned_num_list) or max_residue

    # Run repeated random using solutions and neighbors outlined by prepartition
    for _ in range(num_iter):
        # Get random solution
        p_seq = [random.randint(0,num_elements-1) for _ in range(num_elements)]

        # Recompute the pre-partitioned list of nums and get residue
        prepartitioned_num_list = [0] * num_elements
        for j in range(num_elements):
            prepartitioned_num_list[p_seq[j]] += num_list[j]
        
        min_residue = min(min_residue, karmarkar_karp(prepartitioned_num_list) or max_residue)

    return min_residue

def prepartitioned_hill_climbing(num_list, num_iter):
    num_elements = len(num_list)
    max_residue = sum(num_list)
    p_seq = [random.randint(0,num_elements-1) for _ in range(num_elements)]

    # Get the alternate representation of the input sequence
    prepartitioned_num_list = [0] * num_elements
    for j in range(num_elements):
        prepartitioned_num_list[p_seq[j]] += num_list[j]

    # Get the initial residue of the solution coming from prepartition
    min_residue = karmarkar_karp(prepartitioned_num_list) or max_residue

    # Run repeated random using solutions and neighbors outlined by prepartition
    for _ in range(num_iter):
        # Get random neighbor
        i, j = random.sample(range(num_elements), 2)
        while p_seq[i] == j:
            i, j = random.sample(range(num_elements), 2)
        p_seq[i] = j

        # Recompute the pre-partitioned list of nums and get residue
        prepartitioned_num_list = [0] * num_elements
        for j in range(num_elements):
            prepartitioned_num_list[p_seq[j]] += num_list[j]
        
        min_residue = min(min_residue, karmarkar_karp(prepartitioned_num_list) or max_residue)

    return min_residue

def prepartitioned_simulated_annealing(num_list, num_iter):
    num_elements = len(num_list)
    max_residue = sum(num_list)

    # Start with random solution
    cur_p_seq = [random.randint(0,num_elements-1) for _ in range(num_elements)]

    # Get the alternate representation of the input sequence
    prepartitioned_num_list = [0] * num_elements
    for j in range(num_elements):
        prepartitioned_num_list[cur_p_seq[j]] += num_list[j]

    # Get initial residue
    cur_residue = karmarkar_karp(prepartitioned_num_list) or max_residue
    min_residue = cur_residue

    for t in range(num_iter):
        # Get random neighbor
        neighbor_p_seq = cur_p_seq
        i, j = random.sample(range(num_elements), 2)
        while neighbor_p_seq[i] == j:
            i, j = random.sample(range(num_elements), 2)
        neighbor_p_seq[i] = j

        # Get residue of this random neighbor
        neighbor_num_list = [0] * num_elements
        for j in range(num_elements):
            neighbor_num_list[neighbor_p_seq[j]] += num_list[j]
        neighbor_residue = karmarkar_karp(neighbor_num_list) or max_residue

        # Update current solution and current residue
        if neighbor_residue < cur_residue:
            cur_p_seq = neighbor_p_seq
            cur_residue = neighbor_residue
        else:
            prob = math.exp(-1 * (neighbor_residue - cur_residue) / (t_cooling(t)))
            if random.uniform(0,1) < prob:
                cur_p_seq = neighbor_p_seq
                cur_residue = neighbor_residue

        # Update min residue
        if cur_residue < min_residue:
            min_residue = cur_residue

    return min_residue

def t_cooling(num_iter) -> float:
    return (10 ** 10) * (0.8 ** (num_iter // 300))


def main():
    if len(sys.argv) != 4:
        raise ValueError("Expected usage: python partition.py <flag> <algorithm> <inputfile>")
    else:
        # Command line arguments
        flag = int(sys.argv[1])
        algorithm = int(sys.argv[2])
        inputfile = sys.argv[3]

        # Process input file
        num_list = []
        with open(inputfile, 'r') as f:
            for line in f:
                num = line.strip()
                num_list.append(int(num))

        # Additional parameters
        MAX_ITERATIONS = 5000

        # Normal mode
        if flag == 0:

            # Karmarkar-Karp algorithm
            if algorithm == 0:
                print(karmarkar_karp(num_list))
            
            # Repeated Random algorithm
            elif algorithm == 1:
                print(repeated_random(num_list, MAX_ITERATIONS))

            # Hill Climbing
            elif algorithm == 2:
                print(hill_climbing(num_list, MAX_ITERATIONS))

            # Simulated Annealing    
            elif algorithm == 3:
                print(simulated_annealing(num_list, MAX_ITERATIONS))

            # Prepartitioned Repeated Random algorithm
            elif algorithm == 11:
                print(prepartitioned_repeated_random(num_list, MAX_ITERATIONS))

            # Prepartitioned Hill Climbing algorithm
            elif algorithm == 12:
                print(prepartitioned_hill_climbing(num_list, MAX_ITERATIONS))

            # Prepartitioned Simulated Annealing algorithm
            elif algorithm == 13:
                print(prepartitioned_simulated_annealing(num_list, MAX_ITERATIONS))

        else:
            raise ValueError("Improper flag number (expected: 0)")


if __name__ == "__main__":
    main()
