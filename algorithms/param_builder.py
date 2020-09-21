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
                                dtype=float))[0]

    except ValueError:
        print("Invalid value. Aborting...")


def set_algorithm_parameters(alg_params):
    """
    Interactive function that requests the user to provide
    parameters when asked.
    :param alg_params: Subject Algorithm parameters.
    """

    print("(Input N to skip to the next input)")
    print("(Input Q to abort and save any changes)")

    try:
        user_input = input("GEN - Population Count\n- Current: {}\n- Default: 100\n> "
                           .format(alg_params.population_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.population_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Minimum Generation Count\n- Current: {}\n- Default: 10\n> "
                           .format(alg_params.generation_count_min))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.generation_count_min = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Maximum Generation Count\n- Current: {}\n- Default: 100\n> "
                           .format(alg_params.generation_count_max))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.generation_count_max = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Fitness Evaluator\n"
                           "- 0 = Total Cost\n"
                           "- 1 = Total Distance\n"
                           "- 2 = Longest Route\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.fitness_evaluator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 2:
                while int(user_input) < 0 or int(user_input) > 2:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.fitness_evaluator = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Parent Candidate Count\n- Current: {}\n- Default: 2\n> "
                           .format(alg_params.parent_candidate_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.parent_candidate_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Parent Selection Function\n"
                           "- 0 = Best Fitness\n"
                           "- 1 = Roulette Wheel\n"
                           "- 2 = Tournament\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.parent_selection_function))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 2:
                while int(user_input) < 0 or int(user_input) > 2:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.parent_selection_function = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Selection Probability\n- Current: {}\n- Default: 0.75\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.selection_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.selection_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Offspring Pair Count\n- Current: {}\n- Default: 1\n> "
                           .format(alg_params.offspring_pair_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.offspring_pair_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Crossover Operator\n"
                           "- 0 = 1-Point\n"
                           "- 1 = 2-Point\n"
                           "- 2 = Uniform\n"
                           "- 3 = OE-Children\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.crossover_operator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 3:
                while int(user_input) < 0 or int(user_input) > 3:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.crossover_operator = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Crossover Probability\n- Current: {}\n- Default: 0.90\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.crossover_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.crossover_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Mutation Probability\n- Current: {}\n- Default: 0.05\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.mutation_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.mutation_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Followup Probability\n- Current: {}\n- Default: 0.70\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.followup_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.followup_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Elitism Managing Operator\n"
                           "- 0 = None\n"
                           "- 1 = Retention\n"
                           "- 2 = Filtration\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.elitism_operator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 2:
                while int(user_input) < 0 or int(user_input) > 2:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.elitism_operator = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Elitism Management Rate\n- Current: {}\n- Default: 0\n"
                           "Integer represents how many generations must pass before\n"
                           "elitism managing operator is called.\n"
                           "> "
                           .format(alg_params.elitism_frequency))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.elitism_frequency = int(user_input)
    except ValueError:
        print("Invalid value. Aborting...")
