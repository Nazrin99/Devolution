from program_codes.part1.util.functions import generate_random_candidate, evaluate_fitness, RETAIN_RATIO
import time
from functools import partial
import random
from program_codes import RANDOM_SEED

random.seed(RANDOM_SEED)

def genetic_algorithm(fitness_function, population_size, target_password, crossover_function):
    population = [generate_random_candidate(target_password) for _ in range(population_size)]
    generation = 0
    consecutive_wrong_attempts = 0
    start_time = time.time()
    total_lockout_time = 0
    fitness_function_partial = partial(fitness_function, target_password=target_password)

    while True:
        print(f"Evaluating generation: {generation + 1}")
        fitness_scores = evaluate_fitness(population, fitness_function_partial)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]

        best_candidate = sorted_population[0]
        best_fitness = fitness_function_partial(best_candidate)
        print(f"Best candidate: {best_candidate}\nFitness: ({best_fitness} / {len(target_password)})\n")

        if best_fitness == len(target_password):
            end_time = time.time()
            time_taken = end_time - start_time + total_lockout_time
            return best_candidate, generation, time_taken

        consecutive_wrong_attempts += 1

        if consecutive_wrong_attempts >= 5:
            print(f"Simulating 5-second lockout due to 5 consecutive wrong attempts...\n")
            lockout_start_time = time.time()
            total_lockout_time += 5
            time.sleep(5)  # Simulate the lockout by pausing the program for 5 seconds
            consecutive_wrong_attempts = 0

        retained_population = sorted_population[:int(population_size * RETAIN_RATIO)]
        next_generation = retained_population[:]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(retained_population, 2)
            child = crossover_function(parent1, parent2)
            next_generation.append(child)

        population = next_generation
        generation += 1
