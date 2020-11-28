#!/usr/bin/env python

"""
population_initializers.py:

Collection of functions that are used to initialize a population for the Genetic Algorithm.
"""

import numpy as np
from random import randint, sample, shuffle


def random_solution(**kwargs):
    """
    Generates a random solution to the VRP, although it should be
    noted that its validity is not determined here.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.

    :return: List representation of a random solution to the problem,
    waiting to be assigned to a population individual.
    """

    # Generating a random solution, step 0: Required Variables
    nodes = list(range(kwargs["node_count"]))
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    solution = []

    # Generating a random solution, step 1: Depot Nodes
    selected_depots = [
        depot_nodes[randint(0, len(depot_nodes) - 1)]
        for i in range(vehicle_count)
        ]

    solution = solution + selected_depots

    # Generating a random solution, step 2: Required Nodes
    required_nodes = [i for i in nodes if
                      i not in depot_nodes and
                      i not in optional_nodes]

    solution = solution + required_nodes

    # Generating a random solution, step 3: Optional Nodes
    list_size = max(0, (len(optional_nodes) - len(required_nodes)) // 2)
    add_list = sample(optional_nodes, list_size)
    solution = solution + add_list

    # Generating a random solution, step 4: Shuffle
    shuffle(solution)

    # Generating a random solution, step 5: Move nearest Depot Node to Start
    first_depot = None
    for i in range(len(solution)):
        for j in range(len(depot_nodes)):
            if depot_nodes[j] == solution[i]:
                first_depot = i
                break
        if first_depot is not None:
            break

    solution[0], solution[first_depot] = \
        solution[first_depot], solution[0]

    return solution


def random(**kwargs):
    """
    Creates a population of randomly generated individuals

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    # TODO

    return population


def allele_permutation(**kwargs):
    """
    TODO
    """

    population = []

    # TODO

    return population


def gene_permutation(**kwargs):
    """
    TODO
    """

    population = []

    # TODO

    return population


def simulated_annealing(**kwargs):
    """
    TODO
    """

    population = []

    # TODO

    return population
