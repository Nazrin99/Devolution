import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

# Password to crack
TARGET_PASSWORD = "YTGPl>][Q3C5E#*1nu+`W|Gmjv^nA#"

# Parameters
POPULATION_SIZE = 100  # Reduced for efficiency
MUTATION_RATE = 0.2
GENE_POOL = string.ascii_letters + string.digits + string.punctuation
RETAIN_RATIO = 0.5  # Retain 50% of the population


# Fitness function: Standard monkey problem
def fitness_function(candidate):
    return sum(c == t for c, t in zip(candidate, TARGET_PASSWORD))


# Generate a random individual
def random_individual():
    return ''.join(random.choices(GENE_POOL, k=len(TARGET_PASSWORD)))


# Mutate an individual
def mutate(individual):
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = random.choice(GENE_POOL)
    return ''.join(individual)


# Crossover two parents
def crossover(parent1, parent2):
    split = random.randint(0, len(parent1) - 1)
    return parent1[:split] + parent2[split:]


# Evaluate fitness in parallel
def evaluate_fitness(population, fitness_function):
    with ThreadPoolExecutor() as executor:
        fitness_scores = list(executor.map(fitness_function, population))
    return fitness_scores


# Genetic algorithm
def genetic_algorithm(fitness_function):
    population = [random_individual() for _ in range(POPULATION_SIZE)]
    generation = 0
    consecutive_wrong_attempts = 0  # Track consecutive wrong attempts
    start_time = time.time()  # Track the start time
    total_lockout_time = 0  # Track the total lockout time

    while True:
        print(f"Evaluating generation: {generation + 1}")
        # Evaluate fitness in parallel
        fitness_scores = evaluate_fitness(population, fitness_function)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]

        # Check if solution is found
        best_candidate = sorted_population[0]
        best_fitness = fitness_function(best_candidate)
        print(f"Best candidate: {best_candidate}\nFitness: ({best_fitness} / {len(TARGET_PASSWORD)})\n")

        # If correct password is found
        if best_fitness == len(TARGET_PASSWORD):
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
        retained_population = sorted_population[:int(POPULATION_SIZE * RETAIN_RATIO)]

        # Generate the remaining population using crossover and mutation
        next_generation = retained_population[:]  # Start with the retained population

        # Fill the rest of the population using crossover and mutation
        while len(next_generation) < POPULATION_SIZE:
            parent1, parent2 = random.sample(retained_population, 2)  # Select parents from retained population
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)

        population = next_generation
        generation += 1


# Run the genetic algorithm
print("Running Optimized Genetic Algorithm with Retained Population...")

result, generations, time_taken = genetic_algorithm(fitness_function)
print(
    f"Password cracked: {result} in {generations} generations, Time taken (including lockouts): {time_taken:.2f} seconds.")
