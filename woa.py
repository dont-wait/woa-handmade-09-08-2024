import numpy as np
import random as rd
from plot import plot_solutions_update
from initialize import initialize_solutions
from objective_func import get_info
import math

def calculate_fitness(solutions, fitness_func):
    return np.array([fitness_func(solution) for solution in solutions])

def reset_constant(solutions, lb, ub):
    for i in range(len(solutions)):
        for j in range(len(solutions[i])):
            if solutions[i][j] < ub: solutions[i][j] = ub
            if solutions[i][j] > lb: solutions[i][j] = lb
            
def get_best_solution(solutions, fitness):
    best_index = np.argmin(fitness)
    return solutions[best_index], fitness[best_index]

def calculate_A(a, dim):
    rand = np.random.uniform(0, 1, dim)
    return 2*np.multiply(rand, a) - a

def calculate_C(dim):
    rand = np.random.uniform(0, 1, dim)
    return 2*rand

def Encircling(best_sol, sol, A, dim):
    C = calculate_C(dim)
    D = np.abs(np.multiply(C, best_sol) - sol)
    return best_sol - np.multiply(A, D)

def rand_solution(solutions, population_size):
    return solutions[rd.randint(0, population_size - 1)]

def Searching(rand_sol, sol, A, dim):
    C = calculate_C(dim)
    D = np.abs(np.multiply(C, rand_sol) - sol)
    return rand_sol - np.multiply(A, D)

def Attacking(best_sol, sol, dim, a):
    b = np.random.uniform(-1, 1, dim)
    L = (((1/2*a - 2) - 1) * np.random.uniform(0, 1, dim)) + 1
    D = np.linalg.norm(best_sol - sol)
    return np.multiply(np.multiply(D,np.exp(b*L)), np.cos(2.0*np.pi*L))+best_sol

def update_fitness(solutions, fitness_func, fitness, best_sol):
    fitness_list = calculate_fitness(solutions, fitness_func)
    best_sol_t, fitness_t = get_best_solution(solutions, fitness_list)
    if fitness_t < fitness:
        return fitness_t, best_sol_t
    return fitness, best_sol, 
    
# handle
def woa_handle(function_name, population_size, max_iterater):
    # lay cac fitness, ub, lb, dim
    fitness_func, ub, lb, dim = get_info(function_name)
    # khoi tao quan the ban dau
    solutions = initialize_solutions(population_size, dim, lb, ub)
    # best sol va fitness ban dau
    best_sol = []; fitness = np.inf
    # bat dau
    iter = 0
    while iter < max_iterater:
        # neu co gia tri tot hon thi cap nhat lai
        fitness, best_sol = update_fitness(solutions, fitness_func, fitness, best_sol)
        plot_solutions_update(solutions, best_sol, fitness, ub, lb, iter + 1)
        # lap qua tung ca the va cap nhat vi tri
        a = 2*(1 - iter / max_iterater); i = 0
        new_solutions = np.zeros_like(solutions)
        for solution in solutions:
            p = np.random.uniform(0, 1)
            if p < 0.5:
                A = calculate_A(a, dim)
                if np.linalg.norm(A) < 1:
                    new_solutions[i,:] = Encircling(best_sol, solution, A, dim)
                else:
                    rand_sol = rand_solution(solutions, population_size)
                    new_solutions[i,:] = Searching(rand_sol, solution, A, dim)
            else:
                new_solutions[i,:] = Attacking(best_sol, solution, dim, a)
            i += 1
        solutions = new_solutions
        # neu co ca the vuot khoi khong gian tim kiem thi dat lai gia tri
        reset_constant(solutions, lb, ub)
        iter += 1
    return best_sol, fitness