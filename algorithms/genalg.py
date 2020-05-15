#!/usr/bin/env python

"""
genalg.py:

TODO
"""

from instances.vrp import VRP


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

    vrp.print_solution()

    for i in range(10):
        print("-" * 30)
        vrp.mutate()
        vrp.print_solution()
    pass
