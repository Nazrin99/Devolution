import random
import string
import time

# Target password
target = "G7$pQz!9sW@tL4"

# Parameters
mutation_rate = 0.1
generations = 3000
max_attempts = 5
lockout_time = 5 

# Fitness Function
def fitness(password):
    score = sum(1 for i, c in enumerate(password) if c == target[i])
    return score

# Adaptive Mutation Rate
def adaptive_mutation_rate(fitness_score):
    return mutation_rate * (1 - (fitness_score / len(target)))

# Generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(target)))

# Crossover function (2-point crossover)
def crossover(parent1, parent2):
    crossover_point1 = random.randint(0, len(target) - 1)
    crossover_point2 = random.randint(crossover_point1, len(target))
    
    child = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    return child

# Mutation function
def mutate(password, rate):
    return ''.join(
        c if random.random() > rate else random.choice(string.ascii_letters + string.digits + string.punctuation)
        for c in password
    )

# Fitness Sharing (penalty for similarity)
def fitness_sharing(population):
    shared_fitness = []
    for i, ind1 in enumerate(population):
        fitness_val = fitness(ind1)
        penalty = sum(1 for ind2 in population if ind1 != ind2 and fitness(ind2) == fitness_val)
        shared_fitness.append(fitness_val / (1 + penalty))  # Fitness sharing formula
    return shared_fitness

# Evolutionary Algorithm
def genetic_algorithm(population_size):
    population = [generate_password() for _ in range(population_size)]
    attempts = 0
    failed_attempts = 0
    start_time = time.time()

    for generation in range(generations):
        if failed_attempts >= max_attempts:
            print(f"Locking out for {lockout_time} seconds due to failed attempts.")
            time.sleep(lockout_time)
            failed_attempts = 0
        
        shared_fitness = fitness_sharing(population)
        new_population = []

        for i in range(population_size):
            # Select two parents (using fitness sharing for selection)
            parent1, parent2 = random.choices(population, weights=shared_fitness, k=2)

            # Apply crossover and mutation
            child = crossover(parent1, parent2)
            mutation_rate = adaptive_mutation_rate(shared_fitness[i])
            child = mutate(child, mutation_rate)

            new_population.append(child)
        
        population = new_population
        best_password = max(population, key=fitness)
        if fitness(best_password) == len(target):
            end_time = time.time()
            generations_taken = generation + 1
            runtime = end_time - start_time
            return generations_taken, runtime  # Return generations and runtime in seconds

        attempts += 1
        failed_attempts += 1

    return generations, time.time() - start_time  # If not solved within max generations

# Run the experiment and collect results
def run_experiment():
    experiment_data = []
    
    # Define different configurations for each experiment
    configurations = [
        (50, "two-point", "Part2_1.py"),
        (50, "uniform", "Part2_2.py"),
        (100, "two-point", "Part2_3.py"),
        (100, "uniform", "Part2_4.py"),
        (150, "two-point", "Part2_5.py"),
        (150, "uniform", "Part2_6.py"),
        (200, "two-point", "Part2_7.py"),
        (200, "uniform", "Part2_8.py"),
    ]
    
    for idx, (pop_size, crossover_type, filename) in enumerate(configurations, start=1):
        # Run genetic algorithm and get the generations and runtime
        generations_taken, runtime = genetic_algorithm(pop_size)
        
        # Store the result
        experiment_data.append((idx, "Adaptive Mutation", mutation_rate, crossover_type, pop_size, generations_taken, runtime, filename))

    return experiment_data

# Function to print the experiment table
def print_experiment_table(experiment_data):
    print("| No of Exp | EA Techniques       | Mutation Rate | Crossover Technique | Population Size | Generations to Solve | Time Complexity (seconds) | .py        |")
    print("|-----------|---------------------|---------------|----------------------|-----------------|----------------------|--------------------------|------------|")
    
    for row in experiment_data:
        print(f"| {row[0]:<10} | {row[1]:<20} | {row[2]:<13} | {row[3]:<19} | {row[4]:<15} | {row[5]:<19} | {row[6]:<24} | {row[7]} |")

# Run the experiment and print results
experiment_data = run_experiment()
print_experiment_table(experiment_data)
