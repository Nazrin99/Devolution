import random
import string
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

GENE_POOL = string.ascii_letters + string.digits + string.punctuation
RETAIN_RATIO = 0.5

def monkey_problem_fitness_function(candidate, target_password):
    return sum(c == t for c, t in zip(candidate, target_password))

def generate_random_candidate(target_password):
    return ''.join(random.choices(GENE_POOL, k=len(target_password)))

def mutate_candidate(candidate, mutation_rate):
    candidate = list(candidate)
    for i in range(len(candidate)):
        if random.random() < mutation_rate:
            candidate[i] = random.choice(GENE_POOL)
    return ''.join(candidate)

def one_point_crossover(parent1, parent2):
    split = random.randint(0, len(parent1) - 1)
    return parent1[:split] + parent2[split:]

def evaluate_fitness(population, fitness_function):
    with ThreadPoolExecutor() as executor:
        fitness_scores = list(executor.map(fitness_function, population))
    return fitness_scores

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
            consecutive_wrong_attempts = 0  # Reset the counter after lockout

        # Create next generation
        # Retain 50% of the population (top candidates)
        retained_population = sorted_population[:int(population_size * RETAIN_RATIO)]

        # Generate the remaining population using crossover and mutation
        next_generation = retained_population[:]  # Start with the retained population

        # Fill the rest of the population using crossover and mutation
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(retained_population, 2)  # Select parents from retained population
            child = one_point_crossover(parent1, parent2)
            child = mutate_candidate(child, mutation_rate)
            next_generation.append(child)

        population = next_generation
        generation += 1
