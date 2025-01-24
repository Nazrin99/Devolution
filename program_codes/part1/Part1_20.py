from crossover_only.genetic_algo import genetic_algorithm
from functions import penalized_monkey_problem_fitness_function
from functions import two_point_crossover
from program_codes import TARGET_PASSWORD

POPULATION_SIZE = 100

# Two point crossover only
# Penalized fitness function

if __name__ == '__main__':
    result = genetic_algorithm(penalized_monkey_problem_fitness_function, POPULATION_SIZE, TARGET_PASSWORD, two_point_crossover)

    print(f"\nPassword cracked: {result[0]}\nGeneration: {result[1]}\nTime taken: {result[2]:.2f} seconds")
