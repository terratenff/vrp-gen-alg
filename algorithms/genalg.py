#!/usr/bin/env python

"""
genalg.py:

Runner of the genetic algorithm.
"""

from instances.vrp import VRP
import numpy as np


def run_gen_alg(vrp, alg_params):
    """
    Conducts the Genetic Algorithm on selected VRP type.

    :param vrp: Subject problem to solve.
    :param alg_params: Parameters for the genetic algorithm.
    :return: Computed solution for the VRP.
    """

    # TODO

    population = []
    for i in range(alg_params.population_count):
        instance_copy = VRP(vrp.path_table, vrp.params)
        population.append(instance_copy)

    for individual in population:
        print(str(individual.path_table))

    population[7].path_table = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    for individual in population:
        print(str(individual.path_table))

    return

    vrp.print_solution()

    for i in range(10):
        print("-" * 30)
        vrp.mutate()
        vrp.print_solution()
