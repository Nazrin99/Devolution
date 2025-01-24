import random
import time
from functools import partial

from functions import generate_random_candidate, evaluate_fitness, mutate_candidate, RETAIN_RATIO
from program_codes import RANDOM_SEED

random.seed(RANDOM_SEED)

def genetic_algorithm(fitness_function, population_size, target_password, mutation_rate):
    population = [generate_random_candidate(target_password) for _ in range(population_size)]
    generation = 0
    consecutive_wrong_attempts = 0
    start_time = time.time()
    total_lockout_time = 0
    fitness_function_partial = partial(fitness_function, target_password=target_password)

    while True:
        print(f"Evaluating generation: {generation + 1}")
        # Evaluate fitness in parallel
        fitness_scores = evaluate_fitness(population, fitness_function_partial)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]

        # Check if solution is found
        best_candidate = sorted_population[0]
        best_fitness = fitness_function_partial(best_candidate)
        print(f"Best candidate: {best_candidate}\nFitness: ({best_fitness} / {len(target_password)})\n")

        # If correct password is found
        if best_fitness == len(target_password):
            end_time = time.time()
            time_taken = end_time - start_time + total_lockout_time  # Add lockout time to the total time
            return best_candidate, generation, time_taken

        # Increment wrong attempts counter if the best candidate is incorrect
        consecutive_wrong_attempts += 1

        # Track time for 5 consecutive wrong attempts and simulate the lockout
        if consecutive_wrong_attempts >= 5:
            print(f"Simulating 5-second lockout due to 5 consecutive wrong attempts...\n")
            lockout_start_time = time.time()
            total_lockout_time += 5  # Add 5 seconds for lockout time
            time.sleep(5)  # Simulate the lockout by pausing for 5 seconds
            consecutive_wrong_attempts = 0  # Reset the counter after lockout

        # Create next generation
        # Retain 50% of the population (top candidates)
        retained_population = sorted_population[:int(population_size * RETAIN_RATIO)]

        # Generate the remaining population using mutation only
        next_generation = retained_population[:]  # Start with the retained population

        # Fill the rest of the population using mutation only
        while len(next_generation) < population_size:
            parent = random.choice(retained_population)  # Select a parent from the retained population
            child = mutate_candidate(parent, mutation_rate)  # Mutate the parent
            next_generation.append(child)

        population = next_generation
        generation += 1
