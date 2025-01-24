from mutation_only.genetic_algo import genetic_algorithm
from functions import monkey_problem_fitness_function

TARGET_PASSWORD = "YTGPl>][Q3C5E#*1nu+`W|Gmjv^nA#"
POPULATION_SIZE = 100
MUTATION_RATE = 0.1

if __name__ == '__main__':
    result = genetic_algorithm(monkey_problem_fitness_function, POPULATION_SIZE, TARGET_PASSWORD, MUTATION_RATE)

    print(f"\nPassword cracked: {result[0]}\nGeneration: {result[1]}\nTime taken: {result[2]:.2f} seconds")
