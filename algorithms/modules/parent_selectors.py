#!/usr/bin/env python

"""
parent_selectors.py:

Collection of functions that are used to select candidates for crossover in the population.
"""

import numpy as np
from operator import attrgetter
from random import random, sample


def best_fitness(population, **kwargs):
    """
    Selects two individuals within two population samples that have the best fitness values.

    :param population: Population from which the individuals are chosen.
    :param kwargs: Keyword arguments, from which the following parameters are expected:
    - (int) 'parent_candidate_count': Number of candidates that are selected randomly
      so as to form the population sample.
    - (bool) 'maximize': Flag that determines whether the objective to maximize or minimize.

    :return: Two individuals that have been chosen to be parents, purely based on
    having high fitness value in respective population samples.
    """

    parent_candidate_count = kwargs["parent_candidate_count"]
    maximize = kwargs["maximize"]

    # Create population samples, one for each parent.
    sample1 = sample(population, parent_candidate_count)
    sample2 = sample(population, parent_candidate_count)

    if maximize:
        # Highest fitness value is relevant in VRPP instances.
        parent1 = min(sample1, key=attrgetter("fitness"))
        parent2 = min(sample2, key=attrgetter("fitness"))
    else:
        # Lowest fitness value is relevant in other instances.
        parent1 = max(sample1, key=attrgetter("fitness"))
        parent2 = max(sample2, key=attrgetter("fitness"))

    return parent1, parent2


def roulette_selection(population, **kwargs):
    """
    Selects two individuals within two population samples via roulette wheel selection.

    :param population: Population from which the individuals are chosen.
    :param kwargs: Keyword arguments, from which the following parameters are expected:
    - (int) 'parent_candidate_count': Number of candidates that are selected randomly
      so as to form the population sample.
    - (bool) 'maximize': Flag that determines whether the objective to maximize or minimize.

    :return: Two individuals that have been chosen as parents, based on being victors
    at two different roulette wheel selections.
    """

    parent_candidate_count = kwargs["parent_candidate_count"]
    maximize = kwargs["maximize"]

    # Create population samples, one for each parent.
    sample1 = sample(population, parent_candidate_count)
    sample2 = sample(population, parent_candidate_count)

    # Sorting samples will be necessary in order to make low-fitness-individuals
    # more likely in Roulette Wheel Selection.
    sample1.sort(key=attrgetter("fitness"), reverse=maximize)
    sample2.sort(key=attrgetter("fitness"), reverse=maximize)

    total_fitness1 = sum(x.fitness for x in sample1)
    total_fitness2 = sum(x.fitness for x in sample2)

    if maximize is True:
        probability_set1 = [x.fitness / total_fitness1 for x in sample1]
        probability_set2 = [x.fitness / total_fitness2 for x in sample2]
    else:
        probability_set1 = [1 - (x.fitness / total_fitness1) for x in sample1]
        probability_set2 = [1 - (x.fitness / total_fitness2) for x in sample2]

    # One random float is generated for each sample. Converting probabilities
    # into cumulative probabilities allows easier comparisons.
    probability_set1_cumulative = np.cumsum(probability_set1)
    probability_set2_cumulative = np.cumsum(probability_set2)

    factor1, factor2 = random(), random()
    parent1, parent2 = None, None

    for i in range(len(probability_set1_cumulative)):
        target1 = probability_set1_cumulative[i]
        target2 = probability_set2_cumulative[i]

        if target1 > factor1:
            parent1 = sample1[i]
        if target2 > factor2:
            parent2 = sample2[i]
        if parent1 is not None and parent2 is not None:
            break

    return parent1, parent2


def tournament_selection(population, **kwargs):
    """
    Selects two individuals within two population samples via tournament selection.

    :param population: Population from which the individuals are chosen.
    :param kwargs: Keyword arguments, from which the following parameters are expected:
    - (int) 'parent_candidate_count': Number of candidates that are selected randomly
      so as to form the population sample.
    - (bool) 'maximize': Flag that determines whether the objective to maximize or minimize.
    - (float) 'tournament_probability': A float between 0.00 and 1.00 that determines
      the probability of selecting the winner from the population sample.

    :return: Two individuals that have been chosen as parents, based on being victors
    at two different tournament selections.
    """

    parent_candidate_count = kwargs["parent_candidate_count"]
    maximize = kwargs["maximize"]
    tournament_probability = kwargs["tournament_probability"]

    # Create population samples, one for each parent.
    sample1 = sample(population, parent_candidate_count)
    sample2 = sample(population, parent_candidate_count)

    # Sorting samples will be necessary in order to make low-fitness-individuals
    # more likely in Tournament Selection.
    sample1.sort(key=attrgetter("fitness"), reverse=maximize)
    sample2.sort(key=attrgetter("fitness"), reverse=maximize)

    probability_set_individual = [
        tournament_probability * (1 - tournament_probability) ** k for k in range(parent_candidate_count - 1)
    ]
    last_place = 1.00 - sum(probability_set_individual)
    probability_set_individual.append(last_place)

    # One random float is generated for the sample. Converting probabilities
    # into cumulative probabilities allows easier comparisons.
    probability_set_cumulative = np.cumsum(probability_set_individual)

    factor1, factor2 = random(), random()
    parent1, parent2 = None, None

    for i in range(len(probability_set_cumulative)):
        target = probability_set_cumulative[i]
        
        if target > factor1:
            parent1 = sample1[i]
        if target > factor2:
            parent2 = sample2[i]
        if parent1 is not None and parent2 is not None:
            break

    return parent1, parent2
