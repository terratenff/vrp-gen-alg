#!/usr/bin/env python

"""
utility.py:

Contains convenient function for getting an integer input.
"""


def get_input(min_input=None, max_input=None):
    """
    Convenience function for getting user input.
    :param min_input: Minimum integer input requirement.
    :param max_input: Maximum integer input requirement.
    :return: User input.
    """
    if min_input is not None and max_input is not None:
        def condition(x): return min_input <= x <= max_input
    elif min_input is None:
        def condition(x): return x <= max_input
    elif max_input is None:
        def condition(x): return x >= min_input
    else:
        # noinspection PyUnusedLocal
        def condition(x): return True

    number = None
    while number is None:
        try:
            number = int(input("> "))
            if condition(number) is False:
                print("Input is out of range.")
                number = None
        except ValueError:
            print("Input should be a number.")
            number = None
    return number
