#!/usr/bin/env python

"""
crossover_operators.py:

Collection of functions that are used to breed individuals via crossover in the population.
"""

from copy import deepcopy


def one_point(vrp1, vrp2):
    """
    TODO
    """

    offspring1 = deepcopy(vrp1)
    offspring2 = deepcopy(vrp2)
    offspring1.assign_id()
    offspring2.assign_id()

    return offspring1, offspring2


def two_point(vrp1, vrp2):
    """
    TODO
    """

    offspring1 = deepcopy(vrp1)
    offspring2 = deepcopy(vrp2)
    offspring1.assign_id()
    offspring2.assign_id()

    return offspring1, offspring2


def order_crossover(vrp1, vrp2):
    """
    TODO
    """

    offspring1 = deepcopy(vrp1)
    offspring2 = deepcopy(vrp2)
    offspring1.assign_id()
    offspring2.assign_id()

    return offspring1, offspring2


def vehicle_crossover(vrp1, vrp2):
    """
    TODO
    """

    offspring1 = deepcopy(vrp1)
    offspring2 = deepcopy(vrp2)
    offspring1.assign_id()
    offspring2.assign_id()

    return offspring1, offspring2
