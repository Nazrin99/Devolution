from mutation_crossover.genetic_algo import genetic_algorithm
from functions import penalized_monkey_problem_fitness_function, one_point_crossover
from program_codes import TARGET_PASSWORD

POPULATION_SIZE = 200
MUTATION_RATE = 0.1

# One point crossover with mutation
# Penalized fitness function

if __name__ == '__main__':
    result = genetic_algorithm(penalized_monkey_problem_fitness_function, POPULATION_SIZE, TARGET_PASSWORD, MUTATION_RATE, one_point_crossover)

    print(f"\nPassword cracked: {result[0]}\nGeneration: {result[1]}\nTime taken: {result[2]:.2f} seconds")
