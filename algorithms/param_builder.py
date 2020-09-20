#!/usr/bin/env python

"""
param_builder.py:

Contains functions for setting necessary parameters.
"""

import numpy as np


def set_vrp_parameters(vrp_params):
    """
    Interactive function that requests the user to provide
    parameters when asked.
    :param vrp_params: Subject VRP parameters.
    """

    print("(Input N to skip to the next input)")
    print("(Input Q to abort and save any changes)")

    try:
        user_input = input("VRP - Depot Node\n- Current: {}\n- Default: 0\n> "
                           .format(vrp_params.vrp_depot_node))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_depot_node = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Vehicle Count\n- Current: {}\n- Default: 3\n> "
                           .format(vrp_params.vrp_vehicle_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_vehicle_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Vehicle Variance\n- Current: {}\n- Default: 3\n> "
                           .format(vrp_params.vrp_vehicle_variance))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_vehicle_variance = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Node Service Times\n- Current: {}\n- Default: 0\nInput File Name > "
                           .format(vrp_params.vrp_node_service_time))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_node_service_time = \
                list(np.loadtxt("variables/node_service_times/" + user_input + ".txt",
                                dtype=int))[0]

        # -----------------------------------------------------------------------

        user_input = input("VRP - Distance-to-Time Ratio\n- Current: {}\n- Default: 1\n"
                           "Positive integer: 'n' distance units to 1 time unit\n"
                           "Negative integer: 1 distance unit to 'n' time units\n"
                           "0: 'n' distance units to 0 time units\n> "
                           .format(vrp_params.vrp_distance_time_ratio))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_distance_time_ratio = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("CVRP - Vehicle Capacity\n- Current: {}\n- Default: 0\n> "
                           .format(vrp_params.cvrp_vehicle_capacity))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.cvrp_vehicle_capacity = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("CVRP - Node Demands\n- Current: {}\n- Default: 0\nInput File Name > "
                           .format(vrp_params.cvrp_node_demand))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.cvrp_node_demand = \
                list(np.loadtxt("variables/node_demands/" + user_input + ".txt",
                                dtype=int))[0]

        # -----------------------------------------------------------------------

        user_input = input("OVRP - Enabled\n- Current: {}\n- Default: False\nTrue/False > "
                           .format(vrp_params.ovrp_enabled))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.ovrp_enabled = bool(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRPP - Node Profits\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.vrpp_node_profit))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrpp_node_profit = \
                list(np.loadtxt("variables/node_profits/" + user_input + ".txt",
                                dtype=int))[0]

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Node Time Windows\n- Current: {}\n- Default: None\n"
                           "Input File Name (or 'None') > "
                           .format(vrp_params.vrptw_node_time_window))
        if user_input == "Q":
            return
        elif user_input != "N":
            if user_input.upper() == "NONE":
                vrp_params.vrptw_node_time_window = None
            else:
                vrp_params.vrptw_node_time_window = \
                    list(map(tuple, np.loadtxt("variables/node_time_windows/" + user_input + ".txt",
                                               dtype=int)))

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Node Penalty Coefficients\n- Current: {}\n- Default: 0.00\n"
                           "Input File Name > "
                           .format(vrp_params.vrptw_node_penalty))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrptw_node_penalty = \
                list(np.loadtxt("variables/node_penalties/" + user_input + ".txt",
                                dtype=int))[0]

    except ValueError:
        print("Invalid value. Aborting...")


def set_algorithm_parameters(alg_params):
    """
    Interactive function that requests the user to provide
    parameters when asked.
    :param alg_params: Subject Algorithm parameters.
    """

    # TODO
    pass
