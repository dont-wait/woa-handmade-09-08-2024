import numpy as np

def initialize_solutions(pop_size, dim, lb, ub):
    population = np.random.rand(pop_size, dim) * (ub - lb) + lb
    return population    