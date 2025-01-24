from functions import genetic_algorithm_with_partial_timer, fitness_a

# Password to crack
TARGET_PASSWORD = "G7$pQz!9sW@t"

# Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.1

# Experiment with both fitness functions
print("Running with Fitness Function A (Standard)...")
result_a, generations_a = genetic_algorithm_with_partial_timer(fitness_a, POPULATION_SIZE, TARGET_PASSWORD, MUTATION_RATE)
print(f"Password cracked: {result_a} in {generations_a} generations.")
