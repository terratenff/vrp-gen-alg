#!/usr/bin/env python

"""
matrix_builder.py:

Creates matrices for the VRPs to use.
"""

import numpy as np
from os.path import isdir, exists
from os import makedirs


def generate_matrix():
    """
    Interactive function that guides the user into making a randomized
    path table. It is also named, and once created, stored in the
    "variables" folder.
    :return: Path table of specified node count, randomized elements between
    specified min/max elements. Matrix could be created symmetric or
    asymmetric.
    """

    matrix_name = input("New matrix name > ")
    nodes = int(input("Node count > "))
    minimum = int(input("Minimum element > "))
    maximum = int(input("Maximum element > "))
    symmetric = input("Make a symmetric matrix? (y = yes, <any other input> = no) > ")
    if symmetric.upper() == "Y":
        matr = np.random.randint(minimum, maximum, (nodes, nodes))
        matrix = (matr + matr.T) / 2
    else:
        matrix = np.random.randint(minimum, maximum, (nodes, nodes))
    np.savetxt("variables/" + matrix_name + ".txt", matrix, fmt="%.0f")
    return matrix_name


def load_variable(name, force_load=False):
    """
    Loads a text file from "variables" folder. The text files should
    represent matrices.
    :param name: Name of the text file within the "variables" folder.
    :param force_load: If the loading of specified file fails, then,
    instead of returning nothing, a text file with the specified name
    is created. It is set to be a 10x10 asymmetric matrix with
    elements in range [10,100). Then an attempt is made to load that
    particular text file.
    :return: Matrix from specified text file, or None if file
    reading failed. A random, 10x10 matrix with elements in range
    [10,100) is returned if file loading fails, but force_load flag
    is set to True.
    """

    try:
        var = np.loadtxt("variables/" + name + ".txt")
        return var
    except IOError:
        if force_load is True:
            matrix = np.random.randint(10, 100, (10, 10))
            
            if exists("variables"):
                if isdir("variables") is False:
                    raise EnvironmentError("'variables' keyword is reserved for application variables.")
            else:
                makedirs("variables")

            np.savetxt("variables/" + name + ".txt", matrix, fmt="%.0f")
            return load_variable(name)
        else:
            print("Variable '" + name + "' could not be found.")
            return None


def generate_random_distance_matrix(vrp):
    """
    Creates a random distance matrix for specified VRP.
    An interactive function is called here.
    :param vrp: Subject VRP.
    """

    matrix_file = generate_matrix()
    matrix = load_variable(matrix_file)
    vrp.set_path_table(matrix)
    vrp.table_name = matrix_file


def select_distance_matrix(vrp):
    """
    Selects a distance matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp: Subject VRP.
    """

    matrix_name = input("Target matrix name > ")
    temp_data = load_variable(matrix_name)
    if temp_data is not None:
        vrp.set_path_table(temp_data)
        vrp.table_name = matrix_name
