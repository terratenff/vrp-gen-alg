#!/usr/bin/env python

"""
menu.py:

Maintains a general console menu for the user.
"""

from input_options import mediator


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
    print("1 - Generate random distance matrix")
    print("2 - Select distance matrix")
    print("3 - View current distance matrix")
    print("4 - Set problem parameters")
    print("5 - Set algorithm parameters")
    print("6 - View parameters")
    print("7 - Run genetic algorithm")
    print("-----------------------------------")
    print("(Exit with 0)")

    code = get_input()
    output, vrp_params, alg_params = mediator.inspect(code, vrp_params, alg_params)

    return output, vrp_params, alg_params


def get_input():
    """
    Convenience function for getting user input.
    :return: User input.
    """

    number = None
    while number is None:
        try:
            number = int(input("> "))
        except ValueError:
            print("Input should be a number.")
            number = None
    return number
