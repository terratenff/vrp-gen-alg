#!/usr/bin/env python

"""
vrp_handler.py:

Handles specific parameters of specific VRP types.
"""

from input_options.vrp_inputs.vrp_input import make_instance as make_vrp


def vrp_menu(vrp):
    """
    Interactive menu for handling different types of VRPs
    and unique parameters associated with them.
    :param vrp: Current VRP type.
    :return: Up-to-date VRP type.
    """

    user_input = -1
    while user_input != 0:
        user_input, vrp = vrp_loop(vrp)

    return vrp


def vrp_loop(vrp):
    """
    Interactive loop function for the menu of different VRP types.
    :param vrp: Current VRP type.
    :return: Up-to-date VRP type.
    """

    print("-----------------------------------")
    vrp.print()
    print("-----------------------------------")
    print("Change problem type:")
    print("1 - VRP")
    print("2 - CVRP")
    print("3 - VRPP")
    print("4 - VRPTW")
    print("5 - OVRP")
    print("-----------------------------------")
    print("(Abort type change with 0)")

    code = get_input()
    vrp = inspect(code, vrp)

    return code, vrp


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


def inspect(code, vrp):
    """
    Inspects user input and, in doing so, redirects the
    user to an appropriate course of action.
    :param code: User input.
    :param vrp: Current VRP type.
    :return: Up-to-date VRP type.
    """

    if code == 1:
        vrp = make_vrp(vrp)
    elif code == 2:
        pass
    elif code == 3:
        pass
    elif code == 4:
        pass
    elif code == 5:
        pass

    return vrp
