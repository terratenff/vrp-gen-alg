#!/usr/bin/env python

"""
matrix_builder.py:

TODO
"""

import numpy as np


def generate_matrix():
    matrix_name = input("New matrix name > ")
    nodes = int(input("Node count > "))
    minimum = int(input("Minimum element > "))
    maximum = int(input("Maximum element > "))
    # TODO: Option to make a symmetric matrix.
    matrix = np.random.randint(minimum, maximum, (nodes, nodes))
    np.savetxt("variables/" + matrix_name + ".txt", matrix, fmt="%.0f")
    return matrix_name


def load_variable(name, force_load=False):
    try:
        var = np.loadtxt("variables/" + name + ".txt")
        return var
    except IOError:
        if force_load is True:
            matrix = np.random.randint(10, 100, (10, 10))
            np.savetxt("variables/sample.txt", matrix, fmt="%.0f")
            return load_variable("sample")
        else:
            print("Variable '" + name + "' could not be found.")
            return None


def generate_random_distance_matrix(vrp):
    matrix_file = generate_matrix()
    matrix = load_variable(matrix_file)
    vrp.set_path_table(matrix)


def select_distance_matrix(vrp):
    matrix_name = input("Target matrix name > ")
    temp_data = load_variable(matrix_name)
    if temp_data is not None:
        vrp.set_path_table(temp_data)
        vrp.table_name = matrix_name
