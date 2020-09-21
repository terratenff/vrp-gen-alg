#!/usr/bin/env python

"""
matrix_builder.py:

Creates matrices for the VRPs to use.
"""

import numpy as np


def data_selector(vrp_params, code, sub_code):
    """
    Selector for the function that is specified to be called.
    :param vrp_params: VRP-related parameters.
    :param code: Defines the action that is to be taken with the data.
    :param sub_code: Defines the data type.
    """

    if code == 1:  # Generate
        if sub_code == 1:    # Cost Matrix
            generate_cost_matrix(vrp_params)
        elif sub_code == 2:  # Coordinates
            generate_coordinates_matrix(vrp_params)
        elif sub_code == 3:  # Demands
            generate_demands_matrix(vrp_params)
        elif sub_code == 4:  # Penalties
            generate_penalties_matrix(vrp_params)
        elif sub_code == 5:  # Profits
            generate_profits_matrix(vrp_params)
        elif sub_code == 6:  # Service Times
            generate_service_times_matrix(vrp_params)
        elif sub_code == 7:  # Time Windows
            generate_time_windows_matrix(vrp_params)
    elif code == 2:  # Select
        if sub_code == 1:    # Cost Matrix
            select_cost_matrix(vrp_params)
        elif sub_code == 2:  # Coordinates
            select_coordinates_matrix(vrp_params)
        elif sub_code == 3:  # Demands
            select_demands_matrix(vrp_params)
        elif sub_code == 4:  # Penalties
            select_penalties_matrix(vrp_params)
        elif sub_code == 5:  # Profits
            select_profits_matrix(vrp_params)
        elif sub_code == 6:  # Service Times
            select_service_times_matrix(vrp_params)
        elif sub_code == 7:  # Time Windows
            select_time_windows_matrix(vrp_params)
    elif code == 3:  # View
        if sub_code == 1:    # Cost Matrix
            print(str(vrp_params.vrp_path_table))
        elif sub_code == 2:  # Coordinates
            print(str(vrp_params.vrp_coordinates))
        elif sub_code == 3:  # Demands
            print(str(vrp_params.cvrp_node_demand))
        elif sub_code == 4:  # Penalties
            print(str(vrp_params.vrptw_node_penalty))
        elif sub_code == 5:  # Profits
            print(str(vrp_params.vrpp_node_profit))
        elif sub_code == 6:  # Service Times
            print(str(vrp_params.vrp_node_service_time))
        elif sub_code == 7:  # Time Windows
            print(str(vrp_params.vrptw_node_time_window))


def load_data(name, subdirectory):
    """
    Loads a text file from the variables folder.
    :param name: Name of the text file within the "variables" folder.
    :param subdirectory: Name of the folder inside "variables" that the file is in.
    :return: Matrix from specified text file, or None if file reading failed.
    """

    try:
        var = np.loadtxt("variables/" + subdirectory + "/" + name + ".txt")
        return var
    except IOError:
        print("Variable '" + name + "' could not be found.")
        return None


def generate_cost_matrix(vrp_params):
    """
    Interactive function that guides the user into making a randomized
    path table. It is also named, and once created, stored in the
    "cost_matrices" folder, found in "variables.
    :param vrp_params: VRP parameters, to which the data is added.
    :return: Path table of specified node count, randomized elements between
    specified min/max elements. Matrix could be created symmetric or
    asymmetric.
    """

    matrix_name = input("Cost Matrix Name > ")
    nodes = int(input("Node Count > "))
    minimum = int(input("Minimum Element > "))
    maximum = int(input("Maximum Element > "))
    symmetric = input("Make a Symmetric Matrix? (y/n) > ")
    if symmetric.upper() == "Y":
        matr = np.random.randint(minimum, maximum, (nodes, nodes))
        matrix = (matr + matr.T) / 2
    else:
        matrix = np.random.randint(minimum, maximum, (nodes, nodes))

    np.savetxt("variables/cost_matrices/" + matrix_name + ".txt", matrix, fmt="%.0f")
    matrix = load_data(matrix_name, "cost_matrices")
    vrp_params.set_contents(matrix, name=matrix_name)


def generate_coordinates_matrix(vrp_params):
    """
    Interactive function that guides the user into making a randomized
    list of coordinates. It is also named, and once created, stored in the
    "coordinates" folder, found in "variables".
    :param vrp_params: VRP parameters, to which the data is added.
    :return: List of node coordinates, equaling to specified node count.
    Coordinates are limited by user inputs.
    """

    matrix_name = input("New matrix name > ")
    print("Coordinates will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'coordinates', in 'variables'.")
    nodes = int(input("Node Count > "))
    minimum_x = int(input("Minimum X-Coordinate > "))
    maximum_x = int(input("Maximum X-Coordinate > "))
    minimum_y = int(input("Minimum Y-Coordinate > "))
    maximum_y = int(input("Maximum Y-Coordinate > "))
    matrix1 = np.random.randint(minimum_x, maximum_x, [nodes, 1])
    matrix2 = np.random.randint(minimum_y, maximum_y, [nodes, 1])
    matrix = np.concatenate((matrix1, matrix2), axis=1)

    np.savetxt("variables/coordinates/" + matrix_name + ".txt", matrix, fmt="%.0f")
    matrix = load_data(matrix_name, "coordinates")
    vrp_params.set_contents(matrix, name=matrix_name)
    response = input("Create and save an overriding cost matrix? (y/n) > ")
    if response.upper() == "Y":
        new_name = input("Overriding Cost Matrix Name > ")
        np.savetxt("variables/coordinates/" + new_name + ".txt", vrp_params.vrp_path_table, fmt="%.0f")


def generate_demands_matrix(vrp_params):
    """
    TODO
    :param vrp_params: VRP parameters, to which the data is added.
    :return:
    """
    pass


def generate_penalties_matrix(vrp_params):
    """
    TODO
    :param vrp_params: VRP parameters, to which the data is added.
    :return:
    """
    pass


def generate_profits_matrix(vrp_params):
    """
    TODO
    :param vrp_params: VRP parameters, to which the data is added.
    :return:
    """
    pass


def generate_service_times_matrix(vrp_params):
    """
    TODO
    :param vrp_params: VRP parameters, to which the data is added.
    :return:
    """
    pass


def generate_time_windows_matrix(vrp_params):
    """
    TODO
    :param vrp_params: VRP parameters, to which the data is added.
    :return:
    """
    pass


def select_cost_matrix(vrp_params):
    """
    Selects a cost matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Cost Matrix Name > ")
    temp_data = load_data(matrix_name, "cost_matrices")
    if temp_data is not None:
        vrp_params.set_contents(temp_data, name=matrix_name)
        vrp_params.coordinates_name = None


def select_coordinates_matrix(vrp_params):
    """
    Selects a coordinate list subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Coordinate List Name > ")
    temp_data = load_data(matrix_name, "coordinates")
    if temp_data is not None:
        response = input("Override coordinate list's cost matrix? (y/n) > ")
        if response == "y":
            overriding_matrix_name = input("Overriding Cost Matrix Name > ")
            overriding_temp_data = load_data(matrix_name, "cost_matrices")
            if overriding_temp_data is not None:
                vrp_params.set_contents(temp_data,
                                        path_table_override=overriding_temp_data,
                                        name=overriding_matrix_name)
                vrp_params.coordinates_name = matrix_name
        else:
            print("Calculating path table...")
            vrp_params.set_contents(temp_data, name=matrix_name)
            print("Calculations have finished!")
            vrp_params.coordinates_name = matrix_name


def select_demands_matrix(vrp_params):
    """
    Selects a demands matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Node Demands Matrix Name > ")
    temp_data = load_data(matrix_name, "node_demands")
    if temp_data is not None:
        vrp_params.cvrp_node_demand = temp_data


def select_penalties_matrix(vrp_params):
    """
    Selects a penalties matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Node Penalty Coefficients Matrix Name > ")
    temp_data = load_data(matrix_name, "node_penalties")
    if temp_data is not None:
        vrp_params.vrptw_node_penalty = temp_data


def select_profits_matrix(vrp_params):
    """
    Selects a penalties matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Node Profits Matrix Name > ")
    temp_data = load_data(matrix_name, "node_profits")
    if temp_data is not None:
        vrp_params.vrpp_node_profit = temp_data


def select_service_times_matrix(vrp_params):
    """
    Selects a service times matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Node Service Times Matrix Name > ")
    temp_data = load_data(matrix_name, "node_service_times")
    if temp_data is not None:
        vrp_params.vrp_node_service_time = temp_data


def select_time_windows_matrix(vrp_params):
    """
    Selects a time windows matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    """

    matrix_name = input("Target Node Time Windows Matrix Name > ")
    temp_data = load_data(matrix_name, "node_time_windows")
    if temp_data is not None:
        vrp_params.vrptw_node_time_window = temp_data


def initialize(name):
    """
    Loads a text file from "variables/cost_matrices" folder as part of application
    initialization.
    :param name: Name of the text file within the "variables/cost_matrices" folder.
    :return: Matrix from specified text file, or a randomly generated 10x10 matrix
    with elements in range [10, 100), if file loading fails. The matrix file is
    also created in the process.
    """

    try:
        var = np.loadtxt("variables/cost_matrices/" + name + ".txt")
        return var
    except IOError:
        matrix = np.random.randint(10, 100, (10, 10))
        np.savetxt("variables/cost_matrices/" + name + ".txt", matrix, fmt="%.0f")
        return load_data(name, "cost_matrices")
