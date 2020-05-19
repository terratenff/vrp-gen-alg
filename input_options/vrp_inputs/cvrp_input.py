#!/usr/bin/env python

"""
cvrp_input.py:

Specialized creator of a CVRP.
"""

from instances.vrp_variants.cvrp import CVRP


def make_instance(vrp):
    """
    Creates an instance of a CVRP.
    :param vrp: Current VRP type.
    :return: CVRP.
    """

    path_table = vrp.path_table
    params = vrp.params

    print("Insert vehicle capacity.")
    capacity = int(input("> "))
    new_vrp = CVRP(path_table, params, capacity)

    print("Problem type changed into a CVRP.")

    return new_vrp
