from woa import woa_handle

def main():
    pop_size = 2
    function_name = 'F5'
    max_iterater = 100
    best_sol, fitness_sol = woa_handle(function_name, pop_size, max_iterater)
    print("Giải pháp tốt nhất:", best_sol, fitness_sol)

main()