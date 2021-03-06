#!/usr/bin/env python

"""
matrix_builder.py:

Creates matrices for the VRPs to use.
"""

import numpy as np
from scipy.spatial import distance


def data_selector(vrp_params, code, sub_code):
    """
    Selector for the function that is specified to be called.
    :param vrp_params: VRP-related parameters.
    :param code: Defines the action that is to be taken with the data.
    :param sub_code: Defines the data type.
    """

    if code == 1:  # Generate
        if sub_code == 1:    # Cost Matrix
            generate_cost_matrix()
        elif sub_code == 2:  # Coordinates
            generate_coordinates_matrix()
        elif sub_code == 3:  # Demands
            generate_demands_matrix()
        elif sub_code == 4:  # Penalties
            generate_penalties_matrix()
        elif sub_code == 5:  # Profits
            generate_profits_matrix()
        elif sub_code == 6:  # Service Times
            generate_service_times_matrix()
        elif sub_code == 7:  # Time Windows
            generate_time_windows_matrix()
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
    elif code == 3:  # Deselect
        if sub_code == 1:    # Cost Matrix
            print("Cannot deselect cost matrix!")
        elif sub_code == 2:  # Coordinates
            if vrp_params.vrp_coordinates is None:
                print("Coordinates have been deselected.")
                return
            vrp_params.vrp_coordinates = None
            vrp_params.coordinates_name = None
            vrp_params.cost_matrices_name = "undefined"
            print("Coordinates have been deselected.\nThe cost matrix associated with it remains as-is.")
        elif sub_code == 3:  # Demands
            vrp_params.cvrp_node_demand = None
            vrp_params.node_demands_name = None
            print("Demands have been deselected.")
        elif sub_code == 4:  # Penalties
            vrp_params.vrptw_node_penalty = None
            vrp_params.node_penalties_name = None
            print("Penalties have been deselected.")
        elif sub_code == 5:  # Profits
            vrp_params.vrpp_node_profit = None
            vrp_params.node_profits_name = None
            print("Profits have been deselected.")
        elif sub_code == 6:  # Service Times
            vrp_params.vrp_node_service_time = None
            vrp_params.node_service_times_name = None
            print("Service Times have been deselected.")
        elif sub_code == 7:  # Time Windows
            vrp_params.vrptw_node_time_window = None
            vrp_params.node_time_windows_name = None
            print("Time Windows have been deselected.")
    elif code == 4:  # View
        if sub_code == 1:    # Cost Matrix
            print(str(vrp_params.vrp_path_table).replace("\n  ", " "))
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


def load_data(name, subdirectory, data_type: type = float):
    """
    Loads a text file from the variables folder.
    :param name: Name of the text file within the "variables" folder.
    :param subdirectory: Name of the folder inside "variables" that the file is in.
    :param data_type: Data type of subject data's elements.
    :return: Matrix from specified text file, or None if file reading failed.
    """

    try:
        var = np.loadtxt("variables/" + subdirectory + "/" + name + ".txt", dtype=data_type)
        return var
    except IOError:
        print("Variable '" + name + "' could not be found.")
        return None


def generate_cost_matrix():
    """
    Interactive function that guides the user into making a randomized
    path table. It is also named, and once created, stored in the
    "cost_matrices" folder, found in "variables".
    """

    print("Cost Matrix elements will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'cost_matrices', in 'variables'.")
    matrix_name = input("Cost Matrix Name > ")
    nodes = int(input("Node Count > "))
    minimum = float(input("Minimum Element > "))
    maximum = float(input("Maximum Element (greater than {}) > ".format(minimum)))
    symmetric = input("Make a Symmetric Matrix? (y/n) > ")
    if symmetric.upper() == "Y":
        matr = np.random.uniform(minimum, maximum, (nodes, nodes))
        matrix = (matr + matr.T) / 2
    else:
        matrix = np.random.uniform(minimum, maximum, (nodes, nodes))

    np.savetxt("variables/cost_matrices/" + matrix_name + ".txt", matrix, fmt="%.8f")


def generate_coordinates_matrix():
    """
    Interactive function that guides the user into making a randomized
    list of coordinates. It is also named, and once created, stored in the
    "coordinates" folder, found in "variables".
    """

    print("Coordinates will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'coordinates', in 'variables'.")
    matrix_name = input("Coordinate List Name > ")
    nodes = int(input("Node Count > "))
    minimum_x = float(input("Minimum X-Coordinate > "))
    maximum_x = float(input("Maximum X-Coordinate (greater than {}) > ".format(minimum_x)))
    minimum_y = float(input("Minimum Y-Coordinate > "))
    maximum_y = float(input("Maximum Y-Coordinate (greater than {}) > ".format(minimum_y)))
    matrix1 = np.random.uniform(minimum_x, maximum_x, [nodes, 1])
    matrix2 = np.random.uniform(minimum_y, maximum_y, [nodes, 1])
    matrix = np.concatenate((matrix1, matrix2), axis=1)

    # noinspection PyTypeChecker
    np.savetxt("variables/coordinates/" + matrix_name + ".txt", matrix, fmt="%.8f")
    response = input("Create and save an overriding cost matrix? (y/n) > ")
    if response.upper() == "Y":
        new_name = input("Overriding Cost Matrix Name > ")
        overriding_matrix = distance.cdist(matrix, matrix)
        # noinspection PyTypeChecker
        np.savetxt("variables/cost_matrices/" + new_name + ".txt", overriding_matrix, fmt="%.8f")


def generate_demands_matrix():
    """
    Interactive function that guides the user into making a randomized
    list of node demands. It is also named, and once created, stored in the
    "node_demands" folder, found in "variables".
    """

    print("Demands will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'node_demands', in 'variables'.")
    matrix_name = input("Demand List Name > ")
    nodes = int(input("Node Count > "))
    depot_node_input = str(input("Depot Node [0, {})\n"
                                 "Multiple Depot Nodes can be defined by separating them with whitespace\n"
                                 " > ".format(nodes)))
    depot_node = list(set([int(i) for i in depot_node_input.split(" ")]))
    demand_dimensions = int(input("Number of Capacity Types (Integer, 1 or greater) > "))
    if demand_dimensions < 1:
        print("Number of Capacity types has been set to 1.")
        demand_dimensions = 1
    demand_min = float(input("Minimum Demand > "))
    demand_max = float(input("Maximum Demand (greater than {}) > ".format(demand_min)))
    matrix = np.random.uniform(demand_min, demand_max, [nodes, 1])
    matrix[depot_node] = 0

    for i in range(1, demand_dimensions):
        appendix = np.random.uniform(demand_min, demand_max, [nodes, 1])
        appendix[depot_node] = 0
        matrix = np.concatenate((matrix, appendix), axis=1)

    np.savetxt("variables/node_demands/" + matrix_name + ".txt", matrix, fmt="%.8f")


def generate_penalties_matrix():
    """
    Interactive function that guides the user into making a randomized
    list of node penalty coefficients. It is also named, and once created, stored in the
    "node_penalties" folder, found in "variables".
    """

    print("Penalty Coefficients will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'node_penalties', in 'variables'.")
    matrix_name = input("Penalty Coefficient List Name > ")
    nodes = int(input("Node Count > "))
    depot_node_input = str(input("Depot Node [0, {})\n"
                                 "Multiple Depot Nodes can be defined by separating them with whitespace\n"
                                 " > ".format(nodes)))
    depot_node = list(set([int(i) for i in depot_node_input.split(" ")]))
    penalty_min = float(input("Minimum Penalty Coefficient\n"
                              "- 1.00 is equivalent to time late.\n"
                              "- Low penalty implies low priority\n"
                              "- High penalty implies high priority\n"
                              "- Very high penalty simulates hard time window\n > "))
    penalty_max = float(input("Maximum Penalty Coefficient (greater than {}) > ".format(penalty_min)))
    penalty_depot_min = float(input("Depot Minimum Penalty Coefficient > "))
    penalty_depot_max = float(input("Depot Maximum Penalty Coefficient (greater than {}) > ".format(penalty_depot_min)))
    matrix = np.random.uniform(penalty_min, penalty_max, [nodes, 1])
    matrix_depot = np.random.uniform(penalty_depot_min, penalty_depot_max, [nodes, 1])
    matrix[depot_node] = matrix_depot[depot_node]

    np.savetxt("variables/node_penalties/" + matrix_name + ".txt", matrix, fmt="%.8f")


def generate_profits_matrix():
    """
    Interactive function that guides the user into making a randomized
    list of node profits. It is also named, and once created, stored in the
    "node_profits" folder, found in "variables".
    """

    print("Profits will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'node_profits', in 'variables'.")
    matrix_name = input("Profit List Name > ")
    nodes = int(input("Node Count > "))
    depot_node_input = str(input("Depot Node [0, {})\n"
                                 "Multiple Depot Nodes can be defined by separating them with whitespace\n"
                                 " > ".format(nodes)))
    depot_node = list(set([int(i) for i in depot_node_input.split(" ")]))
    profit_min = float(input("Minimum Profit > "))
    profit_max = float(input("Maximum Profit (greater than {}) > ".format(profit_min)))
    matrix = np.random.uniform(profit_min, profit_max, [nodes, 1])
    matrix[depot_node] = 0

    np.savetxt("variables/node_profits/" + matrix_name + ".txt", matrix, fmt="%.8f")


def generate_service_times_matrix():
    """
    Interactive function that guides the user into making a randomized
    list of node service times. It is also named, and once created, stored in the
    "node_service_times" folder, found in "variables".
    """

    print("Service times will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'node_service_times', in 'variables'.")
    matrix_name = input("Service Time List Name > ")
    nodes = int(input("Node Count > "))
    depot_node_input = str(input("Depot Node [0, {})\n"
                                 "Multiple Depot Nodes can be defined by separating them with whitespace\n"
                                 " > ".format(nodes)))
    depot_node = list(set([int(i) for i in depot_node_input.split(" ")]))
    service_time_min = float(input("Minimum Service Time > "))
    service_time_max = float(input("Maximum Service Time (greater than {}) > ".format(service_time_min)))
    matrix = np.random.uniform(service_time_min, service_time_max, [nodes, 1])
    matrix[depot_node] = 0

    np.savetxt("variables/node_service_times/" + matrix_name + ".txt", matrix, fmt="%.8f")


def generate_time_windows_matrix():
    """
    Interactive function that guides the user into making a randomized
    list of node time windows. It is also named, and once created, stored in the
    "node_time_windows" folder, found in "variables".
    """

    print("Time windows will be generated randomly. If you want to manually edit them,\n"
          "you can edit the text files under the folder 'node_time_windows', in 'variables'.")
    matrix_name = input("Time Window List Name > ")
    nodes = int(input("Node Count > "))
    depot_node_input = str(input("Depot Node [0, {})\n"
                                 "Multiple Depot Nodes can be defined by separating them with whitespace\n"
                                 " > ".format(nodes)))
    depot_node = list(set([int(i) for i in depot_node_input.split(" ")]))
    lower_bound_min = float(input("Minimum Lower Bound Time Window\n"
                                  "(0 or greater) > "))
    lower_bound_max = float(input("Maximum Lower Bound Time Window\n"
                                  "(greater than {}) > ".format(lower_bound_min)))
    upper_bound_min = float(input("Minimum Upper Bound Time Window\n"
                                  "> "))
    upper_bound_max = float(input("Maximum Upper Bound Time Window\n"
                                  "(greater than {}) > ".format(upper_bound_min)))
    depot_time_window_min = float(input("Depot Node Maximum Lower Bound Time Window\n"
                                        "> "))
    depot_time_window_max = float(input("Depot Node Maximum Upper Bound Time Window\n"
                                        "(greater than {}) > ".format(depot_time_window_min)))
    matrix1 = np.random.uniform(lower_bound_min, lower_bound_max, [nodes, 1])
    matrix2 = np.random.uniform(upper_bound_min, upper_bound_max, [nodes, 1])
    matrix = np.concatenate((matrix1, matrix2), axis=1)
    for depot in depot_node:
        depot_upper_bound = np.random.uniform(depot_time_window_min, depot_time_window_max)
        matrix[depot, :] = np.array([0, depot_upper_bound], dtype=float)

    # noinspection PyTypeChecker
    np.savetxt("variables/node_time_windows/" + matrix_name + ".txt", matrix, fmt="%.8f")


def select_cost_matrix(vrp_params, name=None):
    """
    Selects a cost matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    """

    if name is None:
        matrix_name = input("Target Cost Matrix Name > ")
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "cost_matrices")
    if temp_data is not None:
        vrp_params.set_contents(temp_data, name=matrix_name)
        vrp_params.coordinates_name = None


def select_coordinates_matrix(vrp_params, name=None, name_override=None):
    """
    Selects a coordinate list subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    :param name_override: Overriding data file name.
    """

    if name is None:
        matrix_name = input("Target Coordinate List Name > ")
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "coordinates")
    if temp_data is not None:
        if name is None and name_override is None:
            response = input("Override coordinate list's cost matrix? (y/n) > ")
        elif name is not None and name_override is None:
            response = "n"
        else:
            response = "y"

        if response.upper() == "Y":

            if name_override is None:
                overriding_matrix_name = input("Overriding Cost Matrix Name > ")
            else:
                overriding_matrix_name = name_override

            overriding_temp_data = load_data(overriding_matrix_name, "cost_matrices")
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


def select_demands_matrix(vrp_params, name=None):
    """
    Selects a demands matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    """

    if name is None:
        matrix_name = input("Target Node Demands Matrix Name > ")
    elif name == "None":
        vrp_params.cvrp_node_demand = None
        vrp_params.node_demands_name = name
        return
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "node_demands")
    if temp_data is not None:
        vrp_params.cvrp_node_demand = temp_data
        vrp_params.node_demands_name = matrix_name


def select_penalties_matrix(vrp_params, name=None):
    """
    Selects a penalties matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    """

    if name is None:
        matrix_name = input("Target Node Penalty Coefficients Matrix Name > ")
    elif name == "None":
        vrp_params.vrptw_node_penalty = None
        vrp_params.node_penalties_name = name
        return
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "node_penalties")
    if temp_data is not None:
        vrp_params.vrptw_node_penalty = temp_data
        vrp_params.node_penalties_name = matrix_name


def select_profits_matrix(vrp_params, name=None):
    """
    Selects a penalties matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    """

    if name is None:
        matrix_name = input("Target Node Profits Matrix Name > ")
    elif name == "None":
        vrp_params.vrpp_node_profit = None
        vrp_params.node_profits_name = name
        return
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "node_profits")
    if temp_data is not None:
        vrp_params.vrpp_node_profit = temp_data
        vrp_params.node_profits_name = matrix_name


def select_service_times_matrix(vrp_params, name=None):
    """
    Selects a service times matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    """

    if name is None:
        matrix_name = input("Target Node Service Times Matrix Name > ")
    elif name == "None":
        vrp_params.vrp_node_service_time = None
        vrp_params.node_service_times_name = name
        return
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "node_service_times")
    if temp_data is not None:
        vrp_params.vrp_node_service_time = temp_data
        vrp_params.node_service_times_name = matrix_name


def select_time_windows_matrix(vrp_params, name=None):
    """
    Selects a time windows matrix subject to being loaded, for specified VRP.
    This is an interactive function, where the name of
    the text file is requested.
    :param vrp_params: VRP parameters.
    :param name: Data file name.
    """

    if name is None:
        matrix_name = input("Target Node Time Windows Matrix Name > ")
    elif name == "None":
        vrp_params.vrptw_node_time_window = None
        vrp_params.node_time_windows_name = name
        return
    else:
        matrix_name = name
    temp_data = load_data(matrix_name, "node_time_windows")
    if temp_data is not None:
        vrp_params.vrptw_node_time_window = temp_data
        vrp_params.node_time_windows_name = matrix_name


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
        var = np.loadtxt("variables/cost_matrices/" + name + ".txt", dtype=float)
        return var
    except IOError:
        matrix = np.random.uniform(10, 100, (10, 10))
        np.fill_diagonal(matrix, 0)
        np.savetxt("variables/cost_matrices/" + name + ".txt", matrix, fmt="%.8f")
        return load_data(name, "cost_matrices")
