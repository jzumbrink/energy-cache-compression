import sys

import numpy as np
import argparse
import time
from python_algorithms.insertion_sort import *
from python_algorithms.selection_sort import *

start_generate = time.perf_counter()

parser = argparse.ArgumentParser()
parser.add_argument("-n", default=1024)
parser.add_argument("--seed", "-s", default=5)
parser.add_argument("--iterations", "-i", default=10)
parser.add_argument("--builtin", action="store_true")
parser.add_argument("--numpy", action="store_true")
parser.add_argument("--insertion_sort", action="store_true")
parser.add_argument("--selection_sort", action="store_true")

args = parser.parse_args()
n = int(args.n)
seed = int(args.seed)
iterations = int(args.iterations)
if sum([args.builtin, args.numpy, args.insertion_sort, args.selection_sort]) != 1:
    print("[Error] Please choose either builtin, numpy, insertion or selection sort.")
    sys.exit()

# generates the same arrays as the c++ version
rng = np.random.RandomState(seed)
a = (rng.randint(0, 2**32, size=n, dtype=np.uint32) % n).astype(np.uint32)
if args.builtin:
    a = a.tolist()

end_generate = time.perf_counter()

print(f"The random generation of the array a (size={n}) was done in {end_generate - start_generate} s.")

start_sort = time.perf_counter()

for _ in range(iterations):
    b = a.copy()
    if args.builtin or args.numpy:
        b.sort()
    elif args.insertion_sort:
        insertion_sort(b)
    elif args.selection_sort:
        selection_sort(b)

end_sort = time.perf_counter()

print(f"The array a was sorted with {'numpy' if args.numpy else 'builtin'} in {end_sort - start_sort} s.")