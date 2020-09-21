#!/usr/bin/env python

"""
menu.py:

Maintains a general console menu for the user.
"""

from input_options import mediator
from input_options.utility import get_input


def loop(vrp_params, alg_params):
    """
    Loop function for user input and interaction.
    :param vrp_params: VRP parameters.
    :param alg_params: Genetic Algorithm parameters.
    :return: User input and current state of problem instance.
    """

    print("-----------------------------------")
    print("Selected distance matrix: " + vrp_params.content_name)
    print("-----------------------------------")
    print("1 - Generate data")
    print("2 - Select data")
    print("3 - View currently used data")
    print("4 - Set problem parameters")
    print("5 - Set algorithm parameters")
    print("6 - View parameters")
    print("7 - Run genetic algorithm")
    print("-----------------------------------")
    print("(Exit with 0)")

    code = get_input()
    output, vrp_params, alg_params = mediator.inspect(code, vrp_params, alg_params)

    return output, vrp_params, alg_params
