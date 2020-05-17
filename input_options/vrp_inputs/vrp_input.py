#!/usr/bin/env python

"""
vrp_input.py:

Specialized creator of a VRP.
"""

from instances.vrp import VRP


def make_instance(vrp):
    """
    Creates an instance of a VRP.
    :param vrp: Current VRP type.
    :return: Basic VRP.
    """

    path_table = vrp.path_table
    params = vrp.params
    new_vrp = VRP(path_table, params)

    print("Problem type changed into a VRP.")

    return new_vrp
