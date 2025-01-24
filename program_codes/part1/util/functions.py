import random
import string
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from program_codes import RANDOM_SEED

random.seed(RANDOM_SEED)

GENE_POOL = string.ascii_letters + string.digits + string.punctuation
RETAIN_RATIO = 0.5


def penalized_monkey_problem_fitness_function(candidate, target_password):
    penalty = 0

    # Define character types for each position in the target password
    for i, (char, target_char) in enumerate(zip(candidate, target_password)):
        if target_char.isalpha() and not char.isalpha():
            penalty += 1  # Add penalty if target expects alphabet but candidate has non-alphabet
        elif target_char.isdigit() and not char.isdigit():
            penalty += 1  # Add penalty if target expects digit but candidate has non-digit
        elif target_char in "!@#$%^&*()_+-=[]{}|;:,.<>?" and char not in "!@#$%^&*()_+-=[]{}|;:,.<>?":
            penalty += 1  # Add penalty if target expects symbol but candidate has non-symbol

    # The fitness score is the length of the match minus the penalties
    fitness_score = monkey_problem_fitness_function(candidate, target_password)
    return fitness_score - penalty


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


def two_point_crossover(parent1, parent2):
    # Ensure the parents are of equal length
    if len(parent1) != len(parent2):
        raise ValueError("Parents must have the same length")

    # Select two random crossover points
    crossover_point1 = random.randint(1, len(parent1) - 2)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)

    # Create the first offspring by swapping the segments between the crossover points
    offspring1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]

    # Return only the first offspring
    return offspring1

def evaluate_fitness(population, fitness_function):
    with ThreadPoolExecutor() as executor:
        fitness_scores = list(executor.map(fitness_function, population))
    return fitness_scores
