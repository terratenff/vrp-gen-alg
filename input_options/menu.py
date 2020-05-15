#!/usr/bin/env python

"""
menu.py:

TODO
"""

from input_options import mediator


def loop(vrp, alg_params):
    """
    Loop function for user input and interaction.
    :param vrp: Current problem instance being inspected.
    :param alg_params: Genetic Algorithm parameters.
    :return: User input and current state of problem instance.
    """

    print("-----------------------------------")
    print("Selected distance matrix: " + vrp.table_name)
    print("-----------------------------------")
    print("1 - Generate random distance matrix")
    print("2 - Select distance matrix")
    print("3 - View distance matrix")
    print("4 - Set general parameters")
    print("5 - Set problem parameters")
    print("6 - View all parameters")
    print("7 - Run Genetic Algorithm")
    print("-----------------------------------")
    print("(Exit with -1)")

    code = get_input()
    output, vrp = mediator.inspect(code, vrp, alg_params)

    return output, vrp


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
